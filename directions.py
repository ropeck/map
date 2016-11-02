#!/usr/bin/env python
import googlemaps
import os.path, json
from datetime import datetime
from datetime import timedelta
from google.appengine.ext import ndb

class Config(ndb.Model):
  name = ndb.StringProperty()
  value = ndb.StringProperty()

class Mapdirection(ndb.Model):
    arrive = ndb.DateTimeProperty()
    body = ndb.StringProperty(indexed=False)
    delay = ndb.IntegerProperty()
    depart = ndb.DateTimeProperty()
    origin = ndb.StringProperty()
    destination = ndb.StringProperty()
    duration = ndb.IntegerProperty()
#TODO(ropeck) use ndb.GeoPtProperty maybe?

class Directions:
  def __init__(self):
    k = Config.query(Config.name == 'APIKEY').get()
    self.gmaps = googlemaps.Client(key=k.value)

  def directions_api(self, td=datetime.today()):
    return self.gmaps.directions(
                                       "1200 Crittenden Lane, Mountain View CA",
                                       "114 El Camino Del Mar, Aptos CA",
                                       departure_time=td)
  def d(self, k,t='text'):
    return self.leg[k][t]
  def dv(self, k):
    return int(self.d(k,'value'))

  def directions(self, td):
    self.leg = self.directions_api(td)[0]['legs'][0]
    self.duration_in_traffic=self.dv('duration_in_traffic')
    self.duration_in_traffic_text=self.d('duration_in_traffic')
    self.duration = self.dv('duration')
    self.distance_text = self.d('distance')
    self.duration_text = self.d('duration') 
    self.diffstr = "(%+d)" % ((self.duration_in_traffic-self.duration)/60)

    m = Mapdirection(depart=td,
                     origin=self.leg['start_address'],
                     destination=self.leg['end_address'],
                     body=json.dumps(self.leg),
                     duration=self.duration/60,
                     delay=(self.duration_in_traffic-self.duration)/60)
    m.put()

    return self.leg
