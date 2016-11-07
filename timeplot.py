#!/usr/bin/env python
import googlemaps
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

def drawday(td):
  gmaps = directions.Directions()

  d=datetime.today()

  mapdata = [['Time', 'Expected', 'AM Delay', 'PM Delay']]
  data = []
  tdata = []
  mindata = []
  prev=None
  td = td.replace(tzinfo=pytz.timezone("UTC")).astimezone(pytz.timezone('US/Pacific'))
  for f in range(24):
    tdstr = td.strftime("%H:%M")
    directions_result = gmaps.directions(td)
    dur = gmaps.duration/60
    traffic = gmaps.duration_in_traffic/60
    pmdelay = traffic - dur
    if pmdelay < 0:
      dur = dur + pmdelay
      pmdelay = delay * -1

    directions_result = gmaps.directions(td, reverse=True)
    dur = gmaps.duration/60
    traffic = gmaps.duration_in_traffic/60
    amdelay = traffic - dur
    if amdelay < 0:
      dur = dur + amdelay
      amdelay = delay * -1

    mapdata.append([tdstr, dur, amdelay, pmdelay])
    td = td + timedelta(hours=1)
  return mapdata 

@app.route('/plotdata')
@app.route('/plotdata/<date>')
def plotdata(date=None):
  if not date:
    d = datetime.now()
  else:
    d = datetime.fromtimestamp(int(date)/1000)

  mapdata = drawday(d.replace(d.year,d.month,d.day,7,0,0,0))  # midnight Pacific
  dat = json.dumps(mapdata)
  resp = Response(response=dat, \
		status = 200, \
		mimetype="application/json")
  return(resp)

@app.route('/plot')
def plotpage():
  return render_template('timeplot.html')


