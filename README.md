# SaddleTime
## Bicycle-Friendly Bicycle Directions and Route Planning

## *Changes in v1.1*
 - *metric wind mesaurements are not in km/h instead of m/s*


## Implementing on your computer:
```
 git clone https://github.com/kingtor69/saddle-time.git
 python -u venv venv
 pip install -r requirements.txt
```

```
 sudo su postgres
 psql
 CREATE DATABASE saddle_time_db;
 \q
 exit
```

```
 source venv/bin/activate
 python -m seed.py
 flask run
```

## This is also deployed on Heroku: https://saddle-time.herokuapp.com/


### home page displays local weather
 - app.py and helpers.py load default options and will be used to manage user defaults for logged-in users
 - weather.js deals with dynamic changes

### `route` page
 - this is the master route page, offering editability on that page and using different API calls to create new routes in the database or edit existing entries
 - `save` and `update` buttons become available as the features are available
 - if a valid route is entered, but no user is logged in, options to log in or sign up will become available

  **all route data is stored in the queryString, so these routes can be bookmarked and re-loaded without creating a user to save them**

### `user` page
 - shows all publicly available user information to anyone
 - loads image urls saved in the user's profile
 - shows all routes saved by the user
 - allows *only* the logged-in user to delete their user or delete individual routes

## 
## RESTful API calls
These are implemented to gather API information from various sources from JavaScript via Python/Flask.

## `routes` endpoints:
### /api/routes/preview **GET**
This will return routes from the mapbox directions API. 

**required data**

The latitude and longitude for at least 2 checkpoints. *I use n=0 for the start and n=999 for the end of a route,* but that is not necessary except that *0 <= **n** <= 999.* They will be processed in numerical order and regardless of whether latitude comes first or vice versa.
 | key | value |
 | :---: | :--- |
 | *n*-lat | *float number between -90.0 and 90.0* |
 | *n*-lng | *float number between -180.0 and 180.0* |

There must be at least 2 latitude/longitude pairs to return a route.

*example url:* `http://127.0.0.1:5000/api/routes/preview?999-lat=42.32856&999-lng=-83.03999&0-lat=37.746998&0-lng=-122.418653`

### /api/routes **GET** 

Returns a list of all saved routes in the database.

### /api/routes **POST**

Saves a route to the database, with all checkpoints used in the route stored with the order they appear.

**required data****
 - user `id` (automatically passed from the front end if a user is logged in)
 - all checkpoints in order, formatted as in `/api/routes/preview`

**optional data**
 - route `name`
 - checkpoint `name`s *note: these are not currently supported in the front end, but are available in the API calls*
 - measurement `units` ('metric' or 'imperial')

### /api/routes/<route_id> **GET**

Loads a saved route from the mapping APIs (to automatically adjust for construction, *&c.*) This is then parsed in to the query string and loaded in to the `route` page. 

**required data**

The route `id` which is parsed in JavaScript from the route load buttons which appear on a `user`'s page.

### /api/routes/<route_id> **PATCH**

This is accessed in this front end by the `update route` button on the `route` page. It updates the database entry for the route.

**required data**

 - route `id`
 - user `id` (automatically passed from the front end if a user is logged in)
 - all checkpoints in order, formatted as in `/api/routes/preview` *note: even checkpoints that are not changing need to be passed in a **PATCH** request*
 
**optional data**
 - route `name`
 - checkpoint `name`s *note: these are not currently supported in the front end, but are available in the API calls*
 - measurement `units` ('metric' or 'imperial')

### /api/routes/<route_id> **DELETE**
 - permanently deletes a route and all associated checkpoints from the database

## `users` endpoints:
### /api/users **GET**
 - returns a list of all users in the database with publicly available information

### /api/users/<user_id> **GET**
  - returns a single user's information

**required data**
  - user `id`

### /api/users/<user_id> **DELETE**
  - deletes a user from the database permanently

**required data**
  - user `id`
  - logged-in user token from front end

### **POST** and **PATCH** operations are not available via restful APIs at this time


## TESTING
##### Python unittest files are in the `tests` folder
##### I wrote some JS Jasmine tests early on in static/js/tests, but most of the testing was done in Python unittests


## External API information:
APIs used can be found in helpers.py
 | API | environmental variable name | used for: | API docs link |
 | :------- | :------------- | :------------------------------------ | :-------------------------------------------- |
 | Mapquest | MQ_API_KEY = os.environ['MQ_API_KEY'] | elevation data | https://developer.mapquest.com/documentation/open/elevation-api/ |
 | Open Weather Service | OW_API_KEY = os.environ['OW_API_KEY'] | current weather conditions | https://openweathermap.org/current |
 | Mapbox | MB_API_KEY = os.environ['MB_API_KEY'] | maps | https://docs.mapbox.com/api/maps/ |
 |  |  | geocoding | https://docs.mapbox.com/api/search/geocoding/ |
 |  |  | directions | https://docs.mapbox.com/api/navigation/directions/ |

You will need your own tokens. All are free. 