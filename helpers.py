from flask import Flask, request, jsonify
from secrets import ORS_API_KEY, MQ_API_KEY


ORS_API_BASE_URL = "https://api.openrouteservice.org/v2/directions/"
MQ_API_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/"

# TODO: see "should" in docstring:
def geocode_from_location(loc):
    """Returns lattitude and longitute for given location, generally an address. 
    Return False if none found. 
    should Return choices if multiple matches found.
    """
    print(loc)
    resp = request.get(MQ_API_BASE_URL, params={'key': MQ_API_KEY, 'location': loc})
    results = resp.json()["results"]
    if len(results) == 0:
        return False
    elif len(results) > 1:
        codes_list = []
        for i in range(len(results)):
            codes_list.append((results[i]["latLng"]["lat"], results[i]["locations"][0]["latLng"]["lng"]))

    
    return (results[0]["locations"][0]["latLng"]["lat"], results[0]["locations"][0]["latLng"]["lng"])
