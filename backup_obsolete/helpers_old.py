import os
import requests
from flask import session
from models import RouteCheckpoint, User, Route, Checkpoint, RouteCheckpoint

# from urllib2 import urlopen
# from contextlib import closing
# import json

CURR_USER = "logged_in_user"
CURR_ROUTE = "route_in_progress"
CURR_CHECKPOINT_LIST = "checkpoints_in_use"
GUEST = User(username="guest", password="fakepassword")

MQ_API_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/"
OW_API_BASE_URL = "https://api.openweathermap.org/data/2.5/"
WEATHER_ICON_BASE_URL = "http://openweathermap.org/img/wn/"
WEATHER_ICON_SUFFIX = "@2x.png"
MB_API_BASE_URL = "https://api.mapbox.com/"
MB_GEOCODE_BASE_URL = f"{MB_API_BASE_URL}geocoding/v5/mapbox.places/"
MB_DIRECTIONS_BASE_URL = f"{MB_API_BASE_URL}directions/v5/mapbox/"

MQ_API_KEY = os.environ['MQ_API_KEY']
OW_API_KEY = os.environ['OW_API_KEY']
MB_API_KEY = os.environ['MB_API_KEY']

# ORS for future development:
# ORS_API_BASE_URL = "https://api.openrouteservice.org/v2/directions/"
# ORS_API_KEY = os.environ['ORS_API_KEY']

DEFAULT_LOCATION_LOGICAL_NAME = '"Coffee Shop" on Mission St, San Francisco'
DEFAULT_LOCATION = "3139 Mission St, San Francisco, CA 94110"
DEFAULT_LOC_LAT = 37.746998
DEFAULT_LOC_LNG = -122.418653
DEFAULT_UNITS = "imperial"


def unit_markers(units):
    """show unit markers for different unit bases (degrees Celsius vs Farrenheit, etc)"""
    if units=="imperial":
        return ("℉", "mph")
    elif units=="metric":
        return ("℃", "km/h")
    return ("°K", "km/h")

def login_session(user):
    """Log in a registered user to session."""

    session[CURR_USER] = user.id

def logout_session():
    """Remove user who is logging out from session."""

    del session[CURR_USER]


# def get_user_location_from_ip():
#     """retrieve the user's location from their browser/IP address. Return a default location (currently Albuquerque, NM) if location can not be determined."""
#     #!/usr/bin/env python 

#     url = 'http://freegeoip.net/json/'
#     try:
#         with closing(urlopen(url)) as response:
#             location = json.loads(response.read())
#             print(location)
#             location_city = location['city']
#             location_state = location['region_name']
#             location_country = location['country_name']
#             location_zip = location['zipcode']
#     except:
#         return "Albuquerque NM USA 87102"


############################
#### external API calls ####
############################
def geocode_from_location_mq(loc):
    """Uses mapquest API.
    Returns lattitude and longitute for given location. 
    Return False if none found. 
    Returns a list of choices, could be one item long, could be many depending on the search parameters (e.g. searching for 'Albuquerque' yields 2 results: one in NM, USA and one in Brazil).
    """
    resp = requests.get(f'{MQ_API_BASE_URL}address', params={'key': MQ_API_KEY, 'location': loc})
    # return resp
    try: 
        locations = resp.json()["results"][0]["locations"]
        codes_list = []
        for i in range(len(locations)):
            codes_list.append((locations[i]["latLng"]["lat"], locations[i]["latLng"]["lng"]))
        return codes_list

    except:
        return False

def autocomplete_options_from_mapbox(term):
    """uses mapbox autocomplete to return JSON with list of choices formatted for select2"""
    query_url = f'{MB_GEOCODE_BASE_URL}{term}.json?access_token={MB_API_KEY}'
    resp = requests.get(query_url)
    features = resp.json()["features"]
    choices = []
    # TODO: something went wrong in here. e.g. html_id for "Detroit, Michigan, United States" is -83.056742.3487 and *should be* -83.0567c_42.3487
    # I have a redundant workaround to "fix" this, so I'm ignoring it for the moment
    mapbox_geocode = []
    for feature in features:
        mapbox_geocode.append(feature['center'])
        html_id = ""
        for geocode_element in mapbox_geocode:
            html_id = string_from_geocode(list(geocode_element))
        choice = {
            'id': html_id,
            'text': feature['place_name']
        }
        choices.append(choice)
    return {"results": choices}

def geocode_from_location_mb(location):
    """uses mapbox to gather geocode information, returning geocode for the first result in mapbox' format (longitude, latitude) even though that's weird"""
    query_url = f'{MB_GEOCODE_BASE_URL}{location}.json?access_token={MB_API_KEY}'
    print('---------------')
    print(query_url)
    print('---------------')
    resp = requests.get(query_url)
    return resp.json()["features"][0]['center']


def current_weather_from_geocode(geocode, units="metric"):
    """Returns current weather data from OpenWeather API for a geocode, entered as a tuple (lat, lng). Defaults to metric units because cycling, but imperical can be specified by guest and/or saved with registered user profile. In case of error, returns False."""

    try:
        (deg, vel) = unit_markers(units)
        response = requests.get(f'{OW_API_BASE_URL}weather?appid={OW_API_KEY}&lon={geocode[1]}&lat={geocode[0]}&units={units}')
        resp = response.json()
        city = resp["name"]
        conditions = resp["weather"][0]["description"].title()
        weather_icon_url = f'{WEATHER_ICON_BASE_URL}{resp["weather"][0]["icon"]}{WEATHER_ICON_SUFFIX}'
        current_weather_details = {
            "Temperature": f'{round(resp["main"]["temp"], 1)}{deg}',
            "Feels Like": f'{round(resp["main"]["feels_like"], 1)}{deg}',
            "High": f'{round(resp["main"]["temp_max"], 1)}{deg}',
            "Low": f'{round(resp["main"]["temp_min"], 1)}{deg}',
            "Relative Humidity": f'{resp["main"]["humidity"]}%',
            "Wind Speed": f'{round (resp["wind"]["speed"], 1)} {vel}',
            "Wind Direction": f'{resp["wind"]["deg"]}° {wind_direction_logical(resp["wind"]["deg"])}'
        }

        return {
            'city': city, 
            'conditions': conditions, 
            'weather_icon_url': weather_icon_url, 
            'current_weather_details': current_weather_details,
            'units': units
        }
    except: 
        return False

def wind_direction_logical(degrees):
    """Give wind direction a logical name adapted from degrees.
    
    > wind_direction_logical(180) = "Southerly"
    > wind_direction_locical(25) = "Northeasterly"
    """
    if degrees > (360 - 22.5):
        biased_degrees = degrees - 360 + 22.5
    else:
        biased_degrees = degrees + 22.5

    index = int(biased_degrees / 45)
    indices = ["Northerly", "Northeasterly", "Easterly", "Southeasterly", "Southerly", "Southwesterly", "Westerly", "Northwesterly"]
    return indices[index]
    

###### the commended out methods are not being called in app.py
# def check_errors_location(location, error_count):
#     """check for errors in location entry"""
#     errors_location = []
#     if not location:
#         errors_location.append(f'You must request either location or geocode to proceed.')
#         error_count += 1

#     return (errors_location, error_count)

# def check_errors_geocode(lat, lng, error_count):
#     """check for errors in lattitude and longitude entries"""
#     errors_geocode = []
#     if not lat and not lng:
#         errors_geocode.append(f'You must request either location or geocode to proceed.')
#         error_count += 1
#     elif not lat:
#         errors_geocode.append(f'Entered lattitude is "{lat}," which is invalid.')
#         error_count += 1
#     elif not lng:
#         errors_geocode.append(f'Entered longitude is "{lng}," which is invalid.')
#         error_count += 1
#     elif lat > 90 or lat < 0:
#         errors_geocode.append(f'Entered lattitude is "{lat}," which is invalid.')
#         lat = False
#         error_count += 2
#     elif lng > 180 or lng < -180:
#         errors_geocode.append(f'Entered longitude is "{lng}," which is invalid.')
#         lng = False
#         error_count += 2
#     if lat and lng:
#         geocode = (lat, lng)

#     return (errors_geocode, geocode, error_count)

# def geocode_from_mapbox_id(id):
#     """retrieves geocode from mapbox from the place id which is taken from a location search with mapbox"""

def location_from_geocode_mb(lat, lng):
    """retrieves location from mapbox given geocode (in their backwards format"""
    if not lat or not lng:
        return False
    response = requests.get(f'{MB_GEOCODE_BASE_URL}{lng},{lat}.json?access_token={MB_API_KEY}')
    resp = response.json()
    return resp['features'][0]['place_name']
    
    
def string_from_geocode(geocode):
    """creates an html-friendly string from geocode"""
    if not geocode[0] or not geocode[1]:
        return False
    geocode_str = str(geocode)
    html_id = ""
    for char in list(geocode_str):
        if char == "[":
            html_id = html_id
        elif char == "]":
            html_id = html_id
        elif char == ".":
            html_id = html_id + "p"
        elif char == ",":
            html_id = html_id + "c_"
        elif char == " ":
            html_id = html_id
        else:
            html_id = html_id + str(char)
    html_id = html_id +  "c_"
    return html_id

def parse_geocode(arguments):
    """formats geocode for supported services in order of route
    Currently, two services are supported:
        *** ORS is for future development, so written code is commented out ***
        # ORS (Open Route Service):
        #     returns the array ORS expects for route parameters
        #     i.e. f'[[{lat},{lng}],[{lat},{lng}]]
        Mapbox:
            returns string mapbox expects for the route parameters
            i.e. f'{lat},{lng};{lat},{lng};{lat},{lng}'
        NOTE: this method can parse and return data for both services, but is currently only doing so for mapbox (commented out references to geoarray are for ORS)
        """

    # these variables will be the return value
    # geoarray = []
    geostring = ""
    

    # termp variables used to sort everything properly
    id_list = []
    sortable_args = {}
    lat = False
    lng = False
    errors = {}

    for key in arguments:
        value = arguments[key]
        key_split = key.split('-')
        id_int = None
        import pdb
        pdb.set_trace()
        try: 
            id_int = int(key_split[0])
            if not id_int in id_list:
                id_list.append(id_int)
            if not id_int in sortable_args:
                sortable_args[id_int] = {}

            sortable_args[id_int][key_split[1]] = value

        except:
            errors["garbage in garbage out error"] = f"{key} can't be parsed to an id"

    # now build the array and string
    for i in sorted(id_list):
        # geoarray.append([sortable_args[i]['lng'],sortable_args[i]['lat']])
        geostring+=f"{sortable_args[i]['lng']},{sortable_args[i]['lat']};"

    # remove trailing semi-colon
    geostring = geostring[:-1]
    
    if errors:
        return {"errors": errors}

    # return (geoarray, geostring)
    return geostring

# def ORS_directions(geoarray, profile="regular"):
#     """receives coordinates in ORS format([{lng},{lat}],[{lng},{lat}],[&c.]])
#     """
#     url = f'{ORS_DIRECTIONS_BASE_URL}{profile}'

#     resp = requests.post()

def mapbox_directions(coordinates):
    """receives coordinates in mapbox format ({lng},{lat};{lng},{lat},&c.) and returns route data"""

    profile = "cycling"
    url = f'{MB_DIRECTIONS_BASE_URL}{profile}/{coordinates}?alternatives=true&geometries=geojson&steps=true&access_token={MB_API_KEY}'

    resp = requests.get(url)

    return resp.json()