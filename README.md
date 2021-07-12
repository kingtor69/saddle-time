# SaddleTime
## Bicycle-Friendly Bicycle Directions and Route Planning

### Schema & API information:
Schema can be found in schema.sql
APIs to be used can be found in api.py
 - Mapquest: used to geocode locations
 - Open Route Service: provides different routes for different bicycle types:
    - "regular" (referred to as "it's just a bike" in the app)
    - road
    - electric
    - mountain
 - Open Weather: gives weather information (current and forecast) about route location

### TESTING
##### Python unittests need to be moved to root folder to work
##### I wrote some JS Jasmine tests in static/js/tests, but most of the testing was done in Python unittests

### Home page looks good

### Weather API is working:
 - weather.js is working for a location change, but still needs autocomplete to make a better user experience
 - city disappears when changing weather units (why? dunno yet)
   - oh, it's worse than that.... temperatures are all 80.0 F and I don't know where the other numbers came from.
   - drawing board here I come...
 - **and using browser location is not working yet either**

### switched geolocating API from mapquest to mapbox
 - working on autocomplete location entries
 - map styling is good, with three sizes coded in css
 - haven't added any logic for checkpoints yet.
 - icons are downloaded in /static/images/mapbox-icons

### I need to decide how to add new checkpoints. I'm currently setting it up in JavaScript and haven't fixed the styling with that because I might want to move that to Python/Flask