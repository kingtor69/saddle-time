# SaddleTime
## Bicycle-Friendly Bicycle Directions and Route Planning

### Schema & API information:
Schema can be found in schema.sql
APIs to be used can be found in api.py
 - Mapquest: used to geocode locations
 - Open Route Service: provides different routes for different bicycle types:
    - "regular"
    - road
    - electric
    - mountain
 - Open Weather: gives weather information (current and forecast) about route location

### Python unittests are in root folder
 - I'd like to get them in their own folder, but had trouble with `from app import app`
 - further study suggested: blueprints

### JS Jasmine tests were running in static/js/tests and I left some there, but it has been recommended to me to keep my testing limited to Python unittests

### Weather API is working:
 - with hard-coded location
 - weather.js is working for a location change
 - still need to make units selector work to change units
 - and using browser location is not working yet either

### Home page looks good for no logged in user
 - for reasons I've yet to track down, home page becomes users/<int:user_id> when a user logs in

### routes director is giving me some trouble right now
Can not import app information into `user_routes.py` (presumably because `app.py` is one directory *back* from `user_routes.py`)