#!/usr/bin/env python
# [START app]
import googlemaps
from datetime import datetime
from datetime import timedelta
import directions
import logging
import json
from google.appengine.ext import ndb

from flask import Flask

class Mapdirection(ndb.Model):
    arrive = ndb.DateProperty()
    body = ndb.StringProperty(indexed=False)
    delay = ndb.IntegerProperty()
    depart = ndb.DateProperty()
    origin = ndb.StringProperty()
    destination = ndb.StringProperty()
    duration = ndb.IntegerProperty()

app = Flask(__name__)


@app.route('/collectdata')
def hello():

    gmaps = directions.Directions()


    def val(d,key='duration_in_traffic'): 
      return int(d[key]['value'],)

    r = gmaps.directions(datetime.now())

    m = Mapdirection(depart=datetime.now(),
                     origin=r['start_address'],
                     destination=r['end_address'],
                     body=json.dumps(r),
                     duration=val(r,key='duration')/60,
                     delay=(val(r) - val(r,key='duration'))/60)
    m.put()
    return json.dumps(r)




@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.'+str(e), 500
# [END app]
