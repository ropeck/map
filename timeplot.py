#!/usr/bin/env python
import googlemaps
from datetime import datetime
from datetime import timedelta
import numpy as np
import pylab as pl

def gm_init():
    with open('.apikey','r') as f:
          key = f.read().strip()
    return googlemaps.Client(key=key)

gmaps = gm_init()


d=datetime.today()
#d=d.replace(d.year,d.month,31,0,0,0,0)

data = []
tdata = []
mindata = []
for f in range(24*6):
  td = d.replace(d.year,d.month,d.day,d.hour,0,0,0) + timedelta(hours=1)
  td = td + timedelta(minutes=f*10)
  print td
  directions_result = gmaps.directions(
                                     "1200 Crittenden Lane, Mountain View CA",
                                     "114 El Camino Del Mar, Aptos CA",
#                                     alternatives=True,
                                     traffic_model="pessimistic",
                                     departure_time=td)
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
