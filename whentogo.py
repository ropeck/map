#!/usr/bin/env python
import googlemaps
from datetime import datetime
from datetime import timedelta

def directions(td=datetime.now()):
  return gmaps.directions(
                                     "1200 Crittenden Lane, Mountain View CA",
                                     "114 El Camino Del Mar, Aptos CA",
                                     departure_time=td)

def gm_init():
  with open('.apikey','r') as f:
    key = f.read().strip()
  return googlemaps.Client(key=key)

gmaps = gm_init()
  

d=datetime.today()
#d=d.replace(d.year,d.month,31,0,0,0,0)

for f in range(24):
#  td = d.replace(d.year,d.month,d.day,d.hour,0,0,0) + timedelta(hours=1)
  td = d
  td = td + timedelta(minutes=10*f)
  l = directions(td)[0]['legs'][0] # first leg of first result (only one)
  print td, (int(l['duration_in_traffic']['value'])-int(l['duration']['value']))/60, l['duration_in_traffic']['text'], 'vs', l['duration']['text'], l['distance']['text']
    #print  x['legs'][0]['duration']['text'], x['summary']

    # 44 miles normally 0:52
    # cur   17:00 1:12 (+19)
    # 16:50 17:09 1:12 (+19)
    # ...
