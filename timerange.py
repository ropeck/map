#!/usr/bin/env python
import googlemaps
from datetime import datetime
from datetime import timedelta
import directions

gmaps = directions.Directions()

d=datetime.today()
td = d.replace(d.year,d.month,d.day,d.hour,0,0,0)
for f in range(24):
  td = td + timedelta(hours=1)
  print td
  directions_result = gmaps.directions(td)
                                     
  for x in directions_result:
    for l in x['legs']:
      print (int(l['duration_in_traffic']['value'])-int(l['duration']['value']))/60, l['duration_in_traffic']['text'], 'vs', l['duration']['text'], l['distance']['text']
    #print  x['legs'][0]['duration']['text'], x['summary']
  print ""
