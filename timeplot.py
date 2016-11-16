#!/usr/bin/env python
import googlemaps
from google.appengine.api import memcache
from google.appengine import runtime
from datetime import datetime
from datetime import timedelta
import directions

import numpy as np
import pylab as pl
import pytz
import json

import logging
import sys

from flask import Flask, send_file, render_template, Response, request, make_response
from cStringIO import StringIO
import urllib, base64
import matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter
formatter = DateFormatter('%H:%M')

app = Flask(__name__)


@app.route('/drawday/<date>')
def drawdaypage(date):
  dat = json.dumps(drawday(date))
  resp = Response(response=dat, status = 200, mimetype="application/json")
  return(resp)

def drawday(td, reverse=False, cache=True):
  memkey = str(td)
  if reverse:
    memkey = memkey + ":reverse"
  d = memcache.get(memkey)
  if d and cache:
    return d

  gmaps = directions.Directions(origin = request.cookies.get('origin'), destination=request.cookies.get('destination'))

  mapdata = [['Time', 'Expected', 'Delay']]
  if reverse:
    #mapdata = [['Time', 'AM Delay', 'PM Delay']]
    mapdata = [['Time', 'Delay']]

  data = []
  tdata = []
  mindata = []
  prev = None
  td = td.replace(tzinfo=pytz.timezone("UTC")).astimezone(pytz.timezone('US/Pacific'))
  td = td.replace(hour=0, minute=0, second=0)
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
    delay = max(amdelay, pmdelay)

    if reverse:
      mapdata.append([tdstr, delay])
    else:
      mapdata.append([tdstr, dur, delay])

    td = td + timedelta(hours=1)
  memcache.set(memkey, mapdata)
  return mapdata

def drawdaylines(td):
  midnight = td.replace(td.year,td.month,td.day,8,0,0,0)
  memkey = 'lines:'+str(midnight)

# collect the time for the weekly graph
# mapdata for each day, then draw part of them together

  daylist = []
  data = {}
  td = midnight
  for i in range(7):
    day = td.strftime("%a")
    data[day] = drawday(td, reverse=True, cache=False)
    daylist.append(day)
    td = td + timedelta(days=1)

  ret = [['Time'] + daylist]
  try:
    r = 0
    for m in drawday(td)[1:]:
      r = r + 1
      row = [m[0]]
      dn = 1
      for day in daylist:
        row.append(data[day][r][1])
        dn = dn + 1
        ret.append(row)
    memcache.set(memkey, ret)  # maybe use a datastore to cache here?
  except runtime.DeadlineExceededError:
    print "error: deadline exceeded in lookups"
    # the lookups timed out, so the result is probably incomplete
  return ret

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

  #mapdata = drawday(d.replace(d.year,d.month,d.day,8,0,0,0))  # midnight Pacific
  mapdata = drawday(d)
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
  return render_template('travel.html', origin=request.cookies.get('origin'), destination=request.cookies.get('destination'))

@app.route('/traveldata')
@app.route('/traveldata/<date>')
def traveldata(date=None):
  if not date:
    d = datetime.now()
  else:
    d = datetime.fromtimestamp(int(date)/1000)

  mapdata = drawdaylines(d)
  dat = json.dumps(mapdata)
  resp = Response(response=dat, status = 200, mimetype="application/json")
  return(resp)

@app.route('/arrive')
def arrive():
  return render_template('arrive.html')

def timeplus(base, off):
  (hs,ms) = base.split(':')
  return int(ms)+60*int(hs) + off

@app.route('/arrivedata')
@app.route('/arrivedata/<date>')
def arrivedata(date):
  d = datetime.now()
  midnight = d.replace(d.year,d.month,d.day,8,0,0,0)
  data = [['Time', 'Leave', 'Expected', 'Delay']]
  for h in drawday(midnight, cache=False)[1:]:  # skip header
    data.append([timeplus(h[0],0), timeplus(h[0], 0), timeplus(h[0],h[1]), timeplus(h[0],h[2]+h[1])])

  data = json.dumps(data)
  resp = Response(response=data, status = 200, mimetype="application/json")
  return(resp)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
  if request.method == "POST":
    resp = make_response(render_template('settings.html'))
    resp.set_cookie('origin', request.form['origin'])
    resp.set_cookie('destination', request.form['destination'])
    return resp
  else:
    return render_template('settings.html')

@app.route('/layout')
def layout():
  return render_template('layout.html')

# this makes the apikey available to templates in all urls without adding it to the render call
@app.context_processor
def inject_apikey():
  gmap = directions.Directions()
  return dict(apikey=gmap.key)

@app.route('/map')
def map():
  return render_template('map.html')

@app.route('/')
def hello():
  if request.cookies.get('origin') is None:
    origin = "1200 Crittenden Lane, Mountain View CA"
    destination = "114 El Camino Del Mar, Aptos CA"
  else:
    origin = request.cookies.get('origin')
    destination=request.cookies.get('destination')
  gmaps = directions.Directions(origin = origin, destination = destination)
  l = gmaps.directions(None)
  print "steps", gmaps.leg['steps']
  resp = make_response(render_template('index.html', directions=gmaps))
  # check on the cookies
  if request.cookies.get('origin') is None:
    resp.set_cookie('origin', "1200 Crittenden Lane, Mountain View CA")
    resp.set_cookie('destination', "114 El Camino Del Mar, Aptos CA")

  return resp

@app.route('/whentogo')
def whentogo():
  gmaps = directions.Directions()

  d=datetime.today()
  l = gmaps.directions(d)

  old_stdout = sys.stdout
  sys.stdout = mystdout = StringIO()

  print "<pre>"
  print  gmaps.distance_text, 'normally', gmaps.duration_text
  print 'LEAVE ARRIVE NOTES'
  tz = d.replace(tzinfo=pytz.timezone("UTC")).astimezone(pytz.timezone("US/Pacific"))
  print '[now]',(tz+timedelta(minutes=gmaps.duration_in_traffic/60)).strftime("%H:%M"), gmaps.duration_in_traffic_text, gmaps.diffstr
  d=d.replace(d.year,d.month,d.day,d.hour,int(d.minute/10)*10,0,0) + timedelta(minutes=10)
  for f in range(24):
    td = d + timedelta(minutes=10*f)
    l = gmaps.directions(td)
    tz = td.replace(tzinfo=pytz.timezone("UTC")).astimezone(pytz.timezone("US/Pacific"))
    try:
      print tz.strftime("%H:%M"),(tz+timedelta(minutes=gmaps.duration_in_traffic/60)).strftime("%H:%M"), gmaps.duration_in_traffic_text, gmaps.diffstr
    except Exception, e:
      print "error", repr(e)

      # 44 miles normally 0:52
      # now   17:00 1:12 (+19)
      # 16:50 17:09 1:12 (+19)
      # ...
  print "</pre>"
  sys.stdout = old_stdout
  return render_template('whentogo.html', text=mystdout.getvalue())

@app.errorhandler(500)
def server_error(e):
  # Log the error and stacktrace.
  logging.exception('An error occurred during a request.')
  return 'An internal error occurred.'+repr(e), 500
