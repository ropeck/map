#!/usr/bin/env python
from datetime import datetime
from datetime import timedelta
import directions
import string 

gmaps = directions.Directions()

d=datetime.today()
l = gmaps.directions(d)
#print gmaps.distance_text, 'normally', gmaps.duration_text
#print 'LEAVE ARRIVE NOTES'

print  string.join([d.strftime("%H:%M"), (d+timedelta(minutes=gmaps.duration_in_traffic/60)).strftime("%H:%M"),  str(gmaps.duration_in_traffic/60), gmaps.diffstr],
	",")
