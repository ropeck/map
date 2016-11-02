# [START app]
#!/usr/bin/env python
from datetime import datetime
from datetime import timedelta
import directions
import logging

from flask import Flask
from cStringIO import StringIO
import sys
from pytz import timezone

app = Flask(__name__)


@app.route('/whentogo')
def whentogo():
  gmaps = directions.Directions()

  d=datetime.today()
  l = gmaps.directions(d)

  old_stdout = sys.stdout
  sys.stdout = mystdout = StringIO()

  print "<pre>"
  print  gmaps.distance_text, 'normally', gmaps.duration_text
  print 'LEAVE ARRIVE NOTES'
  print '[now]',(d+timedelta(minutes=gmaps.duration_in_traffic/60)).strftime("%H:%M"), gmaps.duration_in_traffic_text, gmaps.diffstr
  d=d.replace(d.year,d.month,d.day,d.hour,int(d.minute/10)*10,0,0) + timedelta(minutes=10)
  for f in range(24):
    td = d + timedelta(minutes=10*f)
    l = gmaps.directions(td)
    tz = td.replace(tzinfo=timezone("UTC")).astimezone(timezone("US/Pacific"))
    print tz.strftime("%H:%M"),(tz+timedelta(minutes=gmaps.duration_in_traffic/60)).strftime("%H:%M"), gmaps.duration_in_traffic_text, gmaps.diffstr

      # 44 miles normally 0:52
      # now   17:00 1:12 (+19)
      # 16:50 17:09 1:12 (+19)
      # ...
  print "</pre>"
  sys.stdout = old_stdout
  return mystdout.getvalue()


@app.errorhandler(500)
def server_error(e):

    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.'+str(e), 500
# [END app]
