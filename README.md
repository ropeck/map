# map

A simple bit of code to look into arrival time projections using
Google Maps Directions API.

## Authentication Note
This code uses an API key which is not checked into the repo.  It's expected to
be in the file '.apikey' in the working directory.

   * TODO() add environment var support for API key too
   * TODO() make the API setup a library shared by the test code
   * TODO() make some testing 
   * TODO() stub out data for testing
   * TODO() graph the arrival time
   * TODO() memcache the data requests
   * TODO() make an app in app engine to run it

# setup
  The lib directory needs to have a copy of the packages used by the app
(Flask, others)

easy_install pip
pip install -t flask googlemaps pytz


