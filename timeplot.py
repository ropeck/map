#!/usr/bin/env python
import googlemaps
from google.appengine.api import memcache
from datetime import datetime
from datetime import timedelta
import directions

import numpy as np
import pylab as pl
import pytz
import json

import logging

from flask import Flask, send_file, render_template, Response
import StringIO
import urllib, base64
import matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter
formatter = DateFormatter('%H:%M')

app = Flask(__name__)

# other plot
#     return render_template('sample.html', var=data)
#

def drawday(td, reverse=False):
  memkey = str(td)
  if reverse:
    memkey = memkey + ":reverse"
  d = memcache.get(memkey)
  if d:
    return d

  gmaps = directions.Directions()

  d=datetime.today()

  mapdata = [['Time', 'Expected', 'Delay']]
  if reverse:
    #mapdata = [['Time', 'AM Delay', 'PM Delay']]
    mapdata = [['Time', 'Delay']]

  data = []
  tdata = []
  mindata = []
  prev = None
  td = td.replace(tzinfo=pytz.timezone("UTC")).astimezone(pytz.timezone('US/Pacific'))
  td = td.replace(hour=0, minute=0)
  for f in range(24):
    tdstr = td.strftime("%H:%M")
    directions_result = gmaps.directions(td)
    dur = gmaps.duration/60
    traffic = gmaps.duration_in_traffic/60
    pmdelay = traffic - dur
    if pmdelay < 0 and not reverse:
      dur = dur + pmdelay
      pmdelay = pmdelay * -1

    directions_result = gmaps.directions(td, reverse=True)
    dur = gmaps.duration/60
    traffic = gmaps.duration_in_traffic/60
    amdelay = traffic - dur
    if amdelay < 0 and not reverse:
      dur = dur + amdelay
      amdelay = amdelay * -1

    if reverse:
      mapdata.append([tdstr, max(amdelay, pmdelay)])
    else:
      mapdata.append([tdstr, dur, pmdelay])
    td = td + timedelta(hours=1)
  memcache.set(memkey, mapdata)
  return mapdata

def drawdaylines(td):
  memkey = 'lines:'+str(td)


  mapdata = [['Time']]

# collect the time for the weekly graph
# mapdata for each day, then draw part of them together
#

  data = []
  for day in range(7):
    m = mapdata(td)
    td = td + datetime.timedelta(days=1)
    data.append(m) # not sure what here...

  memcache.set(memkey, data)  # maybe use a datastore to cache here?
  return data

@app.route('/plotdatarev')
@app.route('/plotdatarev/<date>')
def plotdatarev(date=None):
  if not date:
    d = datetime.now()
  else:
    d = datetime.fromtimestamp(int(date)/1000)

  mapdata = drawday(d.replace(d.year,d.month,d.day,8,0,0,0), reverse=True)  # midnight Pacific
  dat = json.dumps(mapdata)
  resp = Response(response=dat, status = 200, mimetype="application/json")
  return(resp)

@app.route('/plotdata')
@app.route('/plotdata/<date>')
def plotdata(date=None):
  if not date:
    d = datetime.now()
  else:
    d = datetime.fromtimestamp(int(date)/1000)

  mapdata = drawday(d.replace(d.year,d.month,d.day,8,0,0,0))  # midnight Pacific
  dat = json.dumps(mapdata)
  resp = Response(response=dat, status = 200, mimetype="application/json")
  return(resp)

@app.route('/pmplot')
def pmplotpage():
  return render_template('pmplot.html')

@app.route('/plot')
def plotpage():
  return render_template('timeplot.html')

@app.route('/travel')
def travel():
  return render_template('travel.html')

@app.route('/traveldata')
@app.route('/traveldata/<date>')
def traveldata(date=None):
  if not date:
    d = datetime.now()
  else:
    d = datetime.fromtimestamp(int(date)/1000)

  mapdata = drawdaylines(d.replace(d.year,d.month,d.day,8,0,0,0))  # midnight Pacific
  dat = json.dumps(mapdata)
  resp = Response(response=dat, status = 200, mimetype="application/json")
  return(resp)

