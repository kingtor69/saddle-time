import requests
from secrets import ORS_API_KEY, MQ_API_KEY, OW_API_KEY


ORS_API_BASE_URL = "https://api.openrouteservice.org/v2/directions/"
MQ_API_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/"
OW_API_BASE_URL = "api.openweathermap.org/data/2.5/"

# TODO: see "should" in docstring:
def geocode_from_location(loc):
    """Returns lattitude and longitute for given location, generally an address. 
    Return False if none found. 
    should Return list of choices if multiple matches found.
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