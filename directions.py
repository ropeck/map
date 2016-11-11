#!/usr/bin/env python
import googlemaps
import os.path, json
from datetime import datetime
from datetime import timedelta
from google.appengine.ext import ndb
import pytz
import sys

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

class Directions:
  def __init__(self,
                 origin =  "1200 Crittenden Lane, Mountain View CA",
                 destination = "114 El Camino Del Mar, Aptos CA"):
    self.origin = origin
    self.destination = destination
    k = Config.query(Config.name == 'APIKEY').get()
    self.key = k.value
    self.gmaps = googlemaps.Client(key=k.value)


  def d(self, k,t='text'):
    return self.leg[k][t]
  def dv(self, k):
    return int(self.d(k,'value'))

  def directions(self, td, cache=True, reverse=False):
    origin = self.origin
    destination = self.destination

    if reverse:
      save = destination
      destination = origin
      origin = save

    self.duration_in_traffic = 0
    self.duration_in_traffic_text = ''
    self.duration = 0
    self.distance_text = ''
    self.duration_text = ''
    self.diffstr = ''

    if td.tzinfo is None or td.tzinfo.utcoffset(td) is None:
      td = td.replace(tzinfo=pytz.UTC)

    td = td.astimezone(pytz.UTC).replace(tzinfo=None)
    m = Mapdirection.query(Mapdirection.depart == td,
                           Mapdirection.origin == origin,
                           Mapdirection.destination == destination).get()

    if not m and td < datetime.now():  # no data from past
      return

    if not m or cache == False:
      self.leg = self.gmaps.directions(origin, destination,
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
                       origin=origin,
                       destination=destination,
                       body=json.dumps(self.leg),
                       duration=self.duration/60,
                       delay=(self.duration_in_traffic-self.duration)/60)
      try:
        m.put()
      except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "error saving Mapdirection", str(m.depart), exc_value, exc_traceback

    return self.leg
