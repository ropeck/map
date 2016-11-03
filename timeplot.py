#!/usr/bin/env python
import googlemaps
from datetime import datetime
from datetime import timedelta
import directions

import numpy as np
import pylab as pl

import logging

from flask import Flask

app = Flask(__name__)

@app.route('/plot')
def plot():
  gmaps = directions.Directions()

  d=datetime.today()

  data = []
  tdata = []
  mindata = []
  prev=None
  for f in range(24*2):
    td = d.replace(d.year,d.month,d.day,d.hour,0,0,0) + timedelta(hours=1)
    td = td + timedelta(minutes=f*30)
    print td
    directions_result = gmaps.directions(td)
    if prev:
      tdata.append(td)
      mindata.append(gmaps.duration/60)
  #    data.append(gmaps.duration_in_traffic/60-prev)
      data.append(gmaps.duration_in_traffic/60)
    prev = gmaps.duration_in_traffic/60

  #pl.plot_date(mindata, 'bs', data, 'g^')
  #pl.plot_date(tdata, mindata, 'bs')
  pl.plot_date(tdata, data, 'g^-')

#  pl.savefig(sys.stdout, format='png')

  imgdata = StringIO.StringIO()
  pl.savefig(imgdata)
  imgdata.seek(0)  # rewind the data

  print "Content-type: image/png\n"
  uri = 'data:image/png;base64,' + urllib.quote(base64.b64encode(imgdata.buf))
  print '<img src = "%s"/>' % uri
