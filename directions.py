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
  
  def directions(self, td):
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
       
