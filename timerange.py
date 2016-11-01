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
  directions_result = gmaps.directions(td)
                                     
  print td, (gmaps.duration_in_traffic-gmaps.duration)/60,\
	gmaps.duration_in_traffic_text, 'vs', gmaps.duration_text,\
	gmaps.distance_text
