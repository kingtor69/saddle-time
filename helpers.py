import os
import requests
from flask import session, g
from models import RouteCheckpoint, User, Route, Checkpoint, RouteCheckpoint

# from urllib2 import urlopen
# from contextlib import closing
# import json

CURR_USER = "logged_in_user"
CURR_ROUTE = "route_in_progress"
CURR_CHECKPOINT_LIST = "checkpoints_in_use"
GUEST = User(username="guest", password="fakepassword")

ORS_API_BASE_URL = "https://api.openrouteservice.org/v2/directions/"
MQ_API_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/"
OW_API_BASE_URL = "https://api.openweathermap.org/data/2.5/"
WEATHER_ICON_BASE_URL = "http://openweathermap.org/img/wn/"
WEATHER_ICON_SUFFIX = "@2x.png"
MB_API_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

ORS_API_KEY = os.environ['ORS_API_KEY']
MQ_API_KEY = os.environ['MQ_API_KEY']
OW_API_KEY = os.environ['OW_API_KEY']
MB_API_KEY = os.environ['MB_API_KEY']


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

# wait a cotton-pickin' minute:
# since mapbox's key is public anyway, 
# I should do this in JS, yeah?
def autocomplete_options_from_mapbox(location):
    """uses mapbox autocomplete to return JSON with list of choices formatted for select2"""
    query_url = f'{MB_API_BASE_URL}{location}.json?access_token={MB_API_KEY}'
    resp = requests.get(query_url)
    return resp.json()["features"]

def geocode_from_location_mb(location):
    """uses mapbox to gather geocode information"""


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
    

def check_errors_location(location, error_count):
    """check for errors in location entry"""
    errors_location = []
    if not location:
        errors_location.append(f'You must request either location or geocode to proceed.')
        error_count += 1

    return (errors_location, error_count)

def check_errors_geocode(lat, lng, error_count):
    """check for errors in lattitude and longitude entries"""
    errors_geocode = []
    if not lat and not lng:
        errors_geocode.append(f'You must request either location or geocode to proceed.')
        error_count += 1
    elif not lat:
        errors_geocode.append(f'Entered lattitude is "{lat}," which is invalid.')
        error_count += 1
    elif not lng:
        errors_geocode.append(f'Entered longitude is "{lng}," which is invalid.')
        error_count += 1
    elif lat > 90 or lat < 0:
        errors_geocode.append(f'Entered lattitude is "{lat}," which is invalid.')
        lat = False
        error_count += 2
    elif lng > 180 or lng < -180:
        errors_geocode.append(f'Entered longitude is "{lng}," which is invalid.')
        lng = False
        error_count += 2
    if lat and lng:
        geocode = (lat, lng)

    return (errors_geocode, geocode, error_count)