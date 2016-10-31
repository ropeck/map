#!/usr/bin/env python
from datetime import datetime
from datetime import timedelta
import directions
 

gmaps = directions.Directions()

d=datetime.today()
l = gmaps.directions(d)
print gmaps.distance_text, 'normally', gmaps.duration_text
print 'LEAVE ARRIVE NOTES'
print '[now]',(d+timedelta(minutes=gmaps.duration_in_traffic/60)).strftime("%H:%M"), gmaps.duration_in_traffic_text, gmaps.diffstr
d=d.replace(d.year,d.month,d.day,d.hour,int(d.minute/10)*10,0,0) + timedelta(minutes=10)
for f in range(24):
#  td = d.replace(d.year,d.month,d.day,d.hour,0,0,0) + timedelta(hours=1)
  td = d
  td = td + timedelta(minutes=10*f)
  l = gmaps.directions(td)
  print td.strftime("%H:%M"),(td+timedelta(minutes=gmaps.duration_in_traffic/60)).strftime("%H:%M"), gmaps.duration_in_traffic_text, gmaps.diffstr

    # 44 miles normally 0:52
    # now   17:00 1:12 (+19)
    # 16:50 17:09 1:12 (+19)
    # ...
