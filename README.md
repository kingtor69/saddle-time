# SaddleTime
## Bicycle-Friendly Bicycle Directions and Route Planning

## laptop branch
This branch is doing simpler tasks that are easier on RAM and will be merged into main.

### Schema & API information:
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

### TESTING
##### Python unittests need to be moved to root folder to work
##### I wrote some JS Jasmine tests in static/js/tests, but most of the testing was done in Python unittests

### Home page displays local weather
 - app.py and helpers.py load default options and will be used to manage user defaults for logged-in users
 - weather.js deals with dynamic changes
 - future development: option to use browser location

### Route page
 - currently called "new" route page, but I think this will be the master route page, offering editability on that page and using different API calls to create new routes in the database or edit existing entries
 - bicycle type is still an active choice field, but will likely be removed until ORS is implemented
   - (there is definitely need for this functionality: yesterday I was sent over a dirt path on my road bike by google maps)
