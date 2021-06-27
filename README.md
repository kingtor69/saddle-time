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

### Python unittests were working before I changed the schema, but needs to be reworked

### Weather API is working with hard-coded location
 - Still working on javascript to change location. 
   - It partly* works for a location change, not at all for a temperature change.
   - * by which I mean the data is arriving from the API, but not being added to the DOM correctly
 - ...and the javascript to change units is unstarted yet, except a few document.querySelectors

### Home page looks good for no logged in user

### adding Jasmine testing