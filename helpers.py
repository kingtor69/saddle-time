def unit_markers(units):
    """show unit markers for different unit bases (degrees Celsius vs Farrenheit, etc)"""
    if units=="imperial":
        return ("℉", "mph")
    elif units=="metric":
        return ("℃", "km/h")
    return ("°K", "km/h")

def get_user_location_from_ip():
    """retrieve the user's location from their browser/IP address. Return a default location (currently Albuquerque, NM) if location can not be determined."""
    #!/usr/bin/env python 
from urllib2 import urlopen
from contextlib import closing
import json

    url = 'http://freegeoip.net/json/'
    try:
        with closing(urlopen(url)) as response:
            location = json.loads(response.read())
            print(location)
            location_city = location['city']
            location_state = location['region_name']
            location_country = location['country_name']
            location_zip = location['zipcode']
    except:
        return "Albuquerque NM USA 87102"