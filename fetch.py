#!/usr/bin/env python
import googlemaps
from datetime import datetime
from datetime import timedelta

d = datetime.now()

def gm_init():
    with open('.apikey','r') as f:
          key = f.read().strip()
    return googlemaps.Client(key=key)

gmaps = gm_init()


def val(d,key='duration_in_traffic'): 
  print d[0]['legs'][0][key]['text']
  return int(d[0]['legs'][0][key]['value'],)

def time_diff(str,dst):
  returning = gmaps.directions(
                                     "1200 Crittenden Lane, Mountain View CA",
                                     "114 El Camino Del Mar, Aptos CA",
                        departure_time=d)

  return (val(returning) - val(returning,key='duration'))/60
       #print l['duration'], l['distance']
    #print  x['legs'][0]['duration']['text'], x['summary']


print time_diff("1200 Crittenden Lane, Mountain View CA",
                "114 El Camino Del Mar, Aptos CA")
