import os
from flask import session
from models import RouteCheckpoint, User, Route, Checkpoint, RouteCheckpoint

CURR_USER = "logged_in_user"
CURR_ROUTE = "route_in_progress"
CURR_CHECKPOINT_LIST = "checkpoints_in_use"
GUEST = User(username="guest", password="fakepassword")

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

