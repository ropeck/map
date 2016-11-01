#!/usr/bin/env python
import googlemaps
from datetime import datetime
from datetime import timedelta
import directions

import numpy as np
import pylab as pl

gmaps = directions.Directions()


d=datetime.today()
#d=d.replace(d.year,d.month,31,0,0,0,0)

data = []
tdata = []
mindata = []
prev=None
for f in range(24):
  td = d.replace(d.year,d.month,d.day,d.hour,0,0,0) + timedelta(hours=1)
  td = td + timedelta(minutes=f*30)
  print td
  directions_result = gmaps.directions(td)
  if prev:
    tdata.append(td)
    mindata.append(gmaps.duration/60)
    data.append(gmaps.duration_in_traffic/60-prev)
  prev = gmaps.duration_in_traffic/60

print data
#pl.plot_date(mindata, 'bs', data, 'g^')
#pl.plot_date(tdata, mindata, 'bs')
pl.plot_date(tdata, data, 'g^-')
pl.show()
