#!/usr/bin/env python
import googlemaps
from datetime import datetime
from datetime import timedelta

def gm_init():
    with open('.apikey','r') as f:
          key = f.read().strip()
    return googlemaps.Client(key=key)

gmaps = gm_init()

d=datetime.today()
#d=d.replace(d.year,d.month,31,0,0,0,0)

for f in range(24):
  td = d.replace(d.year,d.month,d.day,d.hour,0,0,0)
  td = d + timedelta(hours=f)
  print td
  directions_result = gmaps.directions(
                                     "1200 Crittenden Lane, Mountain View CA",
                                     "114 El Camino Del Mar, Aptos CA",
#                                     alternatives=True,
                                     traffic_model="pessimistic",
                                     departure_time=td)
  for x in directions_result:
    for l in x['legs']:
      print (int(l['duration_in_traffic']['value'])-int(l['duration']['value']))/60, l['duration_in_traffic']['text'], 'vs', l['duration']['text'], l['distance']['text']
    #print  x['legs'][0]['duration']['text'], x['summary']
  print ""
