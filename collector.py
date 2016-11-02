#!/usr/bin/env python
# [START app]
import googlemaps
from datetime import datetime
from datetime import timedelta
import directions
import logging
import json

from flask import Flask


app = Flask(__name__)


@app.route('/collectdata')
def hello():

    gmaps = directions.Directions()
    # to make the most useful cached data, we want to make the time rounded but app engine cron can run
    # the script anytime.  So, zero out the end of the time to make it nice.
    dt = datetime.now()
    dt = dt.replace(dt.year,dt.month,dt.day,dt.hour,int(dt.minute/10)*10,0,0) + timedelta(minutes=10)
    r = gmaps.directions(dt)
    return json.dumps(r)




@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.'+str(e), 500
# [END app]
