#!/usr/bin/env python
# [START app]
import googlemaps
from datetime import datetime
from datetime import timedelta
import directions
import logging
from google.appengine.ext import ndb

from flask import Flask

class Mapdirection(nbd.model):
    arrive = nbd.DatetimeProperty()
    body = nbd.StringProperty()
    delay = nbd.IntegerProperty()
    depart = nbd.DatetimeProperty()
    origin = nbd.StringProperty()
    destination = nbd.StringProperty()
    duration = nbd.IntegerProperty()
    

app = Flask(__name__)


@app.route('/collectdata')
def hello():

    gmaps = directions.Directions()


    def val(d,key='duration_in_traffic'): 
      return int(d[key]['value'],)

    r = gmaps.directions(datetime.today())

    m = Mapdirection(depart=datetime.today(),
                     delay=(val(r) - val(r,key='duration'))/60,
                     body=str(r))
    m.put()
    return str(m)




@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
