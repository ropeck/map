# [START app]
#!/usr/bin/env python
from datetime import datetime
from datetime import timedelta
import directions
import logging

from flask import Flask, render_template
from cStringIO import StringIO
import sys
from pytz import timezone

app = Flask(__name__)




@app.errorhandler(500)
def server_error(e):

    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.'+str(e), 500
# [END app]
