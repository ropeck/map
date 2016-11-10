# [START app]
import logging

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/sample')
def sample():
    return render_template('sample.html')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
