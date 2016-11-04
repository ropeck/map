#!/usr/bin/env python
import googlemaps
from datetime import datetime
from datetime import timedelta
import directions

import numpy as np
import pylab as pl
import pytz

import logging

from flask import Flask, send_file, render_template
import StringIO
import urllib, base64
import matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter
formatter = DateFormatter('%H:%M')

app = Flask(__name__)

@app.route('/plot')
# other plot
#     return render_template('sample.html', var=data)
#

def plot():
  gmaps = directions.Directions()

  d=datetime.today()

  mapdata = [['Time', 'Delay', 'Drive Time']]
  data = []
  tdata = []
  mindata = []
  prev=None
  td = d.replace(d.year,d.month,d.day,7,0,0,0)  # midnight Pacific
  #td = td.replace(tzinfo=pytz.timezone("UTC"))
  for f in range(24):
    td = td + timedelta(hours=1)
    tdstr = td.strftime("%H:%M")
    directions_result = gmaps.directions(td)
    dur = gmaps.duration/60
    traffic = gmaps.duration_in_traffic/60
    delay = traffic - dur
    mapdata.append([tdstr, delay, traffic])

  return render_template('timeplot.html', data=mapdata)
