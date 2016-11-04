# [START app]
import logging

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def hello():
    return '<h2>Map App</h2><a href="/whentogo">whentogo</a> <br><iframe src="/plot" style="width: 80%; height: 600px frameBorder: 0"></iframe>'

@app.route('/sample')
def sample():
    return render_template('sample.html')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
