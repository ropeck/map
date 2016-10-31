#!/usr/bin/env python
from datetime import datetime
from datetime import timedelta
import directions
 

gmaps = directions.Directions()

d=datetime.today()
d=d.replace(d.year,d.month,d.day,d.hour,int(d.minute/10)*10,0,0) + timedelta(minutes=10)
l = gmaps.directions(d)[0]['legs'][0] # first leg of first result (only one)
diffstr = "(%+d)" % ((int(l['duration_in_traffic']['value'])-int(l['duration']['value']))/60)
print l['distance']['text'], 'normally', l['duration']['text']
print 'LEAVE ARRIVE NOTES'
print '[now]',(d+timedelta(minutes=int(l['duration_in_traffic']['value'])/60)).strftime("%H:%M"), l['duration_in_traffic']['text'], diffstr
for f in range(24):
#  td = d.replace(d.year,d.month,d.day,d.hour,0,0,0) + timedelta(hours=1)
  td = d
  td = td + timedelta(minutes=10*f)
  l = gmaps.directions(td)[0]['legs'][0] # first leg of first result (only one)
  diffstr = "(%+d)" % ((int(l['duration_in_traffic']['value'])-int(l['duration']['value']))/60)
  print td.strftime("%H:%M"),(td+timedelta(minutes=int(l['duration_in_traffic']['value'])/60)).strftime("%H:%M"), l['duration_in_traffic']['text'], diffstr
    #print  x['legs'][0]['duration']['text'], x['summary']

    # 44 miles normally 0:52
    # now   17:00 1:12 (+19)
    # 16:50 17:09 1:12 (+19)
    # ...
