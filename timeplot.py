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
for f in range(24*6):
  td = d.replace(d.year,d.month,d.day,d.hour,0,0,0) + timedelta(hours=1)
  td = td + timedelta(minutes=f*10)
  print td
  directions_result = gmaps.directions(td)
  for x in directions_result:
    for l in x['legs']:
      tdata.append(td)
      mindata.append(int(l['duration']['value'])/60)
      data.append(int(l['duration_in_traffic']['value'])/60)

print data
#pl.plot_date(mindata, 'bs', data, 'g^')
pl.plot_date(tdata, mindata, 'bs')
pl.plot_date(tdata, data, 'g^')
pl.show()
