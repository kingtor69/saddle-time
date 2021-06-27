import requests
from secret import ORS_API_KEY, MQ_API_KEY, OW_API_KEY
from helpers import unit_markers

ORS_API_BASE_URL = "https://api.openrouteservice.org/v2/directions/"
MQ_API_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/"
OW_API_BASE_URL = "https://api.openweathermap.org/data/2.5/"
WEATHER_ICON_BASE_URL = "http://openweathermap.org/img/wn/"
WEATHER_ICON_SUFFIX = "@2x.png"

def geocode_from_location(loc):
    """Returns lattitude and longitute for given location, generally an address. 
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

def current_weather_from_geocode(geocode, units="metric"):
    """Returns current weather data from OpenWeather API for a geocode, entered as a tuple. Defaults to metric units because cycling, but a logged in and registered user will be able to specify imperial."""
    (deg, vel) = unit_markers(units)
    response = requests.get(f'{OW_API_BASE_URL}weather?appid={OW_API_KEY}&lon={geocode[1]}&lat={geocode[0]}&units={units}')
    resp = response.json()
    city = resp["name"]
    conditions = resp["weather"][0]["description"].title()
    weather_icon_url = f'{WEATHER_ICON_BASE_URL}{resp["weather"][0]["icon"]}{WEATHER_ICON_SUFFIX}'
    current_weather_details = {
        "Temperature": f'{resp["main"]["temp"]}{deg}',
        "Feels Like": f'{resp["main"]["feels_like"]}{deg}',
        "High": f'{resp["main"]["temp_max"]}{deg}',
        "Low": f'{resp["main"]["temp_min"]}{deg}',
        "Relative Humidity": f'{resp["main"]["humidity"]}%',
        "Wind Speed": f'{resp["wind"]["speed"]} {vel}',
        "Wind Direction": f'{resp["wind"]["deg"]}° {wind_direction_logical(resp["wind"]["deg"])}'
    }

    return {
        'city': city, 
        'conditions': conditions, 
        'weather_icon_url': weather_icon_url, 
        'current_weather_details': current_weather_details
    }

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