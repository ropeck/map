# [START app]
import logging

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def hello():
    return '<h2>Map App</h2><p><a href="/travel">travel</a><br><a href="/whentogo">whentogo<br><iframe src="/plot" style="width: 80%; height: 600px; border: none"></iframe><p><iframe src="/whentogo" style="width: 90%; height: 800px; border: none"></iframe></a><p>'

@app.route('/sample')
def sample():
    return render_template('sample.html')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
