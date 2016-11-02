#!/usr/bin/env python
import googlemaps
from datetime import datetime
from datetime import timedelta
import directions

gmaps = directions.Directions()


def val(d,key='duration_in_traffic'): 
  return int(d[key]['value'],)

def time_diff(str,dst):
  returning = gmaps.directions(datetime.today())

  return (val(returning) - val(returning,key='duration'))/60


print time_diff("1200 Crittenden Lane, Mountain View CA",
                "114 El Camino Del Mar, Aptos CA")
