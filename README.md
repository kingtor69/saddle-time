# SaddleTime
## Bicycle-Friendly Bicycle Directions and Route Planning

## Implementing on your computer (directions for linux computer, things that can be skipped for other OSes are *noted as such*):
 git clone https://github.com/kingtor69/saddle-time.git
 python -u venv venv
 pip install -r requirements.txt
 *sudo su postgres*
 psql
 CREATE DATABASE saddle_time_db;
 \q
 psql < seed.py
 exit
 source venv/bin/activate
 flask run

## deployed on Heroku: https://saddle-time.herokuapp.com/


## Schema & API information:
Schema can be found in schema.sql
APIs to be used can be found in api.py
 - Open Weather: gives weather information (current and forecast) about route location
 - Mapbox: used for:
   - maps
   - geocoding (forward and reverse)
   - bicycle directions (one-size fits all)
 - Mapquest: currently unused
 - Open Route Service: currently unused, but for future development, provides different routes for different bicycle types:
    - "regular" (referred to as "it's just a bike" in the app)
    - road
    - electric
    - mountain

## TESTING
##### Python unittest files are in the root folder
##### I wrote some JS Jasmine tests in static/js/tests, but most of the testing was done in Python unittests

## Home page displays local weather
 - app.py and helpers.py load default options and will be used to manage user defaults for logged-in users
 - weather.js deals with dynamic changes
 - future development: option to use browser location

## Route page
 - currently called "new" route page, but I think this will be the master route page, offering editability on that page and using different API calls to create new routes in the database or edit existing entries
 - bicycle type is in the WTForm, but is inactive until ORS is implemented
   - there is definitely need for this functionality: 
     - yesterday I was sent over a dirt path on my road bike by google maps
     - it appears from some testing I've done that mapbox is likely to do the same thing
     - ORS' "regular" bike seems to do it, too

## RESTful API calls
These are currently being used to gather API information from various sources from JavaScript via Python/Flask.

### endpoints:
#### /api/routes/preview
This will return routes from the mapbox directions API. 

****required data****

The latitude and longitude for at least 2 checkpoints. *I use n=0 for the start and n=999 for the end of a route.* They will be processed in numerical order and regardless of whether latitude comes first or vice versa.
 | key | value |
 | :---: | :--- |
 | *n*-lat | *float number between -90.0 and 90.0* |
 | *n*-lng | *float number between -180.0 and 180.0* |

*example url:* `http://127.0.0.1:5000/api/routes/preview?999-lat=42.32856&999-lng=-83.03999&0-lat=37.746998&0-lng=-122.418653`