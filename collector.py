#!/usr/bin/env python
# [START app]
import googlemaps
from datetime import datetime
from datetime import timedelta
import directions
import logging

from flask import Flask


app = Flask(__name__)


@app.route('/collectdata')
def hello():

    gmaps = directions.Directions()

    r = gmaps.directions(datetime.now())
    return json.dumps(r)




@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.'+str(e), 500
# [END app]
