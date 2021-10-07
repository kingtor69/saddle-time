import os
import requests
from flask import session
from models import CheckpointRoute, User, Route, Checkpoint, CheckpointRoute
from datetime import datetime

#######################
## helpful variables ##
#######################
CURR_USER = "logged_in_user"
CURR_ROUTE = "route_in_progress"
CURR_CHECKPOINT_LIST = "checkpoints_in_use"
GUEST = User(username="guest", password="fakepassword")

MQ_GEOCODE_BASE_URL =f"http://www.mapquestapi.com/geocoding/v1/"
MQ_ELEVATION_BASE_URL = f"http://open.mapquestapi.com/elevation/v1/profile"
OW_API_BASE_URL = "https://api.openweathermap.org/data/2.5/"
WEATHER_ICON_BASE_URL = "http://openweathermap.org/img/wn/"
WEATHER_ICON_SUFFIX = "@2x.png"
MB_API_BASE_URL = "https://api.mapbox.com/"
MB_GEOCODE_BASE_URL = f"{MB_API_BASE_URL}geocoding/v5/mapbox.places/"
MB_DIRECTIONS_BASE_URL = f"{MB_API_BASE_URL}directions/v5/mapbox/"
MB_MATCHING_BASE_URL = f"{MB_API_BASE_URL}matching/v5/mapbox/"

MQ_API_KEY = os.environ['MQ_API_KEY']
OW_API_KEY = os.environ['OW_API_KEY']
MB_API_KEY = os.environ['MB_API_KEY']

DEFAULT_LOCATION_LOGICAL_NAME = '"Coffee Shop" on Mission St, San Francisco'
DEFAULT_LOCATION = "3139 Mission St, San Francisco, CA 94110"
DEFAULT_LOC_LAT = 37.746998
DEFAULT_LOC_LNG = -122.418653
DEFAULT_UNITS = "imperial"

STOCK_PROFILE_PICS = ["quino-al-kZgjAT6bbIA-unsplash.jpg", "greg-trowman-o_bdxmF6n24-unsplash.jpg", "viktor-bystrov-8WGscMKJ6bU-unsplash.jpg"]
STOCK_BIKE_PICS = ["aditya-wardhana-LFv9vVBLmwM-unsplash.jpg", "ridley_dream.jpg", "saddletime-default-bike.png", "jacek-dylag-fZglO1JkwoM-unsplash.jpg", "patrick-hendry-qDBbM9Erwo4-unsplash.jpg", "dmitrii-vaccinium-9qsK2QHidmg-unsplash.jpg"]

#############################
## login/logout of session ##
#############################
def login_session(user):
    """Log in a registered user to session."""
    session[CURR_USER] = user.id

def logout_session():
    """Remove user who is logging out from session."""
    del session[CURR_USER]

########################
## external API calls ##
########################
def geocode_from_location_mq(loc):
    """Uses mapquest API.
    Returns lattitude and longitute for given location. 
    Return False if none found. 
    Returns a list of choices, could be one item long, could be many depending on the search parameters (e.g. searching for 'Albuquerque' yields 2 results: one in NM, USA and one in Brazil).
    """
    resp = requests.get(f'{MQ_API_BASE_URL}address', params={'key': MQ_API_KEY, 'location': loc})
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
    resp = requests.get(query_url)
    return resp.json()["features"][0]['center']

def location_from_geocode_mb(lat, lng):
    """retrieves location from mapbox given geocode (in their backwards format"""
    if not lat or not lng:
        return False
    response = requests.get(f'{MB_GEOCODE_BASE_URL}{lng},{lat}.json?access_token={MB_API_KEY}')
    resp = response.json()
    return resp['features'][0]['place_name']
    
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

def mapbox_directions(coordinates):
    """receives coordinates in mapbox format ({lng},{lat};{lng},{lat},&c.) and returns route data"""
    profile = "cycling"
    url_directions = f'{MB_DIRECTIONS_BASE_URL}{profile}/{coordinates}?alternatives=true&geometries=geojson&steps=true&access_token={MB_API_KEY}'
    resp_directions = requests.get(url_directions)
    directions_data_json = resp_directions.json()
    return directions_data_json

def mapquest_elevation(directions_data):
    """gets elevation information from Mapquest given data from the routes acquired from Mapbox
    """
    lat_lng_collection = ""
    for route in directions_data['routes']:
        lat_lng_collection = stringify_mb_coordinates_for_mq(route['geometry']['coordinates'])
        url_elevation = f"{MQ_ELEVATION_BASE_URL}?key={MQ_API_KEY}&shapeFormat=raw&latLngCollection={lat_lng_collection}"
        resp_elevation = requests.get(url_elevation)
        route['geometry']['elevation'] = resp_elevation.json()
    return (directions_data)

def mapbox_matching(route_geometry):
    """receives route geometry data as an ordered list and returns route data matched to mapbox's street grid"""
    profile = "cycling"
    coordinates = ""
    for waypoint in route_geometry:
        coordinates += f'{waypoint[0]},{waypoint[1]};'
    coordinates = coordinates[:-1]
    url_matching = f'{MB_MATCHING_BASE_URL}{profile}/{coordinates}?access_token={MB_API_KEY}'
    resp_matching = requests.get(url_matching)
    return resp_matching.json()

##################
## misc helpers ##
##################
def unit_markers(units):
    """show unit markers for different unit bases (degrees Celsius vs Farrenheit, etc)"""
    if units=="imperial":
        return ("℉", "mph")
    elif units=="metric":
        return ("℃", "m/s")
    return ("°K", "m/s")

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
    input arguments are formated in a dict as such:
        { 
            0-lat: "42.2917",
            0-lng: "-85.5872",
            999-lat: "42.3487",
            999-lng: "-83.0567"
        }
    returns string mapbox requires for the route parameters
    i.e. '-85.5872,42.2917;-83.0567,42.3487'
    """
    geostring = ""
    id_list = []
    sortable_args = {}
    lat = False
    lng = False
    errors = {}
    for key in arguments:
        # ignores non-geocode arguments
        if key.find('lat') >= 0 or key.find('lng') >= 0:
            value = arguments[key]
            key_split = key.split('-')
            id_int = None
            try: 
                id_int = int(key_split[0])
                if not id_int in id_list:
                    id_list.append(id_int)
                if not id_int in sortable_args:
                    sortable_args[id_int] = {}
                sortable_args[id_int][key_split[1]] = value
            except:
                errors["garbage in garbage out error"] = f"{key} can't be parsed to an id"
    for i in sorted(id_list):
        geostring+=f"{sortable_args[i]['lng']},{sortable_args[i]['lat']};"
    geostring = geostring[:-1]
    if errors:
        return {"errors": errors}
    return geostring

def stringify_mb_coordinates_for_mq(geoarray): 
    geostring = ""
    for geocode in geoarray:
        geostring += f"{geocode[1]},{geocode[0]},"
    geostring = geostring[:-1]
    return geostring

def logical_date_time(timestamp):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    hour = timestamp.hour
    am_or_pm = "AM"
    if hour >= 12:
        am_or_pm = "PM"
    if hour > 12:
        hour -= 12
    if hour == 0:
        hour = 24

    return f'{timestamp.year} {months[timestamp.month]} {timestamp.day}, {hour}:{timestamp.minute}{am_or_pm}'

def is_today_april_fools():
    now=datetime.now()
    today = now.strftime("%D")
    today_split = today.split('/')
    if today_split[0] == "04" and today_split[1] == "01":
        return True
    return False