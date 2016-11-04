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
    created = ndb.DateTimeProperty(auto_now=True)
    
#TODO(ropeck) use ndb.GeoPtProperty maybe?

class Directions:
  def __init__(self):
    k = Config.query(Config.name == 'APIKEY').get()
    self.gmaps = googlemaps.Client(key=k.value)


  def d(self, k,t='text'):
    return self.leg[k][t]
  def dv(self, k):
    return int(self.d(k,'value'))

  def directions(self, td, cache=True):
    ORIGIN = "1200 Crittenden Lane, Mountain View CA"
    DESTINATION = "114 El Camino Del Mar, Aptos CA"
    m = Mapdirection.query(Mapdirection.depart == td,
                           Mapdirection.origin == ORIGIN,
                           Mapdirection.destination == DESTINATION).get()

    if not m or cache == False:
      self.leg = self.gmaps.directions(ORIGIN, DESTINATION,
                                       departure_time=td)[0]['legs'][0]
    else:
      self.leg = json.loads(m.body)

    self.duration_in_traffic=self.dv('duration_in_traffic')
    self.duration_in_traffic_text=self.d('duration_in_traffic')
    self.duration = self.dv('duration')
    self.distance_text = self.d('distance')
    self.duration_text = self.d('duration')
    self.diffstr = "(%+d)" % ((self.duration_in_traffic-self.duration)/60)

    if not m:                   # save the data if it's not in the datastore
      m = Mapdirection(depart=td,
                       origin=ORIGIN,
                       destination=DESTINATION,
                       body=json.dumps(self.leg),
                       duration=self.duration/60,
                       delay=(self.duration_in_traffic-self.duration)/60)
      m.put()

    return self.leg
