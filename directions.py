#!/usr/bin/env python
import googlemaps
import os.path, json
from datetime import datetime
from datetime import timedelta

 
class Directions:
  def __init__(self):
    with open('.apikey','r') as f:
      key = f.read().strip()
    self.gmaps = googlemaps.Client(key=key)

  def directions_api(self, td=datetime.today()):
    return self.gmaps.directions(
                                       "1200 Crittenden Lane, Mountain View CA",
                                       "114 El Camino Del Mar, Aptos CA",
                                       departure_time=td)
  
  def directions_json(self, td):
    path = "directions/"+str(td)+".api"
    result = ""
    if os.path.exists(path):
      with open(path,'r') as f:
        result = json.load(f)
    else:
      result = self.directions_api(td)
      with open(path,'w') as f:
        json.dump(result, f)
    return result

  def d(self, k,t='text'):
    return self.leg[k][t]
  def dv(self, k):
    return int(self.d(k,'value'))

  def directions(self, td):
    self.leg = self.directions_json(td)[0]['legs'][0]
    self.duration_in_traffic=self.dv('duration_in_traffic')
    self.duration_in_traffic_text=self.d('duration_in_traffic')
    self.duration = self.dv('duration')
    self.distance_text = self.d('distance')
    self.duration_text = self.d('duration') 
    self.diffstr = "(%+d)" % ((self.duration_in_traffic-self.duration)/60)
    return self.leg 
