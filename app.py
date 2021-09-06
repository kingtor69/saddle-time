import os

from flask import Flask, request, redirect, render_template, flash, jsonify, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User, Route, Checkpoint
from forms import RouteForm, UserNewForm, LoginForm, NewCheckpointForm, LocationForm
from helpers import *

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///saddle_time_db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "really_very_secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.before_request
def add_user_to_g():
    """If user is logged in, add that user to `g`; 
    otherwise, add guest user object to `g`."""

    if CURR_USER in session:
        g.user = User.query.get(session[CURR_USER])
    else:
        g.user = GUEST

@app.before_request
def add_route_to_g():
    """If there is a route in progress, add it to `g`;
    otherwise, add empty route object to `g`."""

    if CURR_ROUTE in session:
        g.route = Route.query.get(session[CURR_ROUTE])




@app.route('/', methods=["GET"])
def load_home_page():
    """Loads home page.
    If there is a logged in user, page shows weather from user's default location and most recently created route.
    If no one is logged in, page shows weather from default location (Albuquerque, NM because that's my joint) in metric units (because cycling). Offer the user option to change the location (including to their browser's location) and the units. (Location change handled in app.js; units change handled hear)
    """
    # default values: 
    location = DEFAULT_LOCATION
    loc_lat = DEFAULT_LOC_LAT
    loc_lng = DEFAULT_LOC_LNG
    units = DEFAULT_UNITS
    if 'location' in request.args:
        location = request.args['location']
    else:
        try:
            location = g.user.location
        except:
            flash(f'using default location ({DEFAULT_LOCATION_LOGICAL_NAME})', 'info')
    if 'latitude' in request.args and 'longitute' in request.args:
        loc_lat = request.args['latitude']
        loc_lng = request.args['longitute']
    else:
        [loc_lng, loc_lat] = geocode_from_location_mb(location)
    
    if 'units' in request.args:
        units = request.args['units']
    else:
        try:
            units = g.user.units
        except:
            flash('using default temperature and distance units (imperial)', 'info')

    weather = current_weather_from_geocode([loc_lat, loc_lng], units)

    return render_template('home.html', weather=weather, lng=loc_lng, lat=loc_lat, location=location, weather_units=units)

#####################################
##### location & weather routes #####
#####################################
@app.route('/api/location', methods=["GET"])
def location_autocomplete():
    """retrieves location options from mapbox autocomplete
    accepting select2 data which comes in as 'term'
    returns list of options from mapbox autocomplete for select2"""
    if request.args['term']:
        term = request.args['term']
        return jsonify(autocomplete_options_from_mapbox(term))

    """or returns reverse geocode location mapbox when passed 'lat' and 'lng'"""
    results = {'results': {}}
    if request.args['lat'] and request.args['lng']:
        try:
            results = location_from_geocode_mb(request.args['lng'], request.args['lat'])
        except:
            results['results']['Errors'] =  {"Geocoding error": "Invalid geocode entered."}

    if request.args['term']:
        try:
            term = request.args['term']
            results = autocomplete_options_from_mapbox(term)
        except:
            results['results']['Errors'] = {"Geocoding error": "No results found for that search term."}

    return jsonify(results)


@app.route('/api/geocode', methods=["GET"])
def geocode_location():
    try: 
        location = request.args['location']
        return jsonify(geocode_from_location_mq(request.args['location']))
    except:
        return {"results": {"Errors": {"Geocoding error": "Invalid location entered."}}}

@app.route('/api/weather', methods=["GET"])
def retrieve_weather_data_from_geocode():
    """gather weather data from units & geocode input
    NOTE: the geocode used by the weather API is lat-lng whereas mapbox uses lng-lat, and that's one reason this accepts latitude and longitude as separate arguments."""
    # TODO: needs error managing

    units = request.args['units']
    geocode = (request.args['lat'], request.args['lng'])
    return jsonify(current_weather_from_geocode(geocode, units))


#######################
##### user routes #####
#######################
@app.route('/users/signup', methods=["GET", "POST"])
def signup_new_user():
    """Sign up new users. Enter into database"""

    form = UserNewForm()
    if form.validate_on_submit():
        new_user = User.hashpass(form.username.data, form.password.data)
        new_user.email = form.email.data
        new_user.first_name = form.first_name.data
        new_user.last_name = form.last_name.data
        new_user.profile_pic_image_url = form.profile_pic_image_url.data
        new_user.fav_bike = form.fav_bike.data
        new_user.bike_image_url = form.bike_image_url.data
        new_user.default_bike_type = form.default_bike_type.data
        new_user.weather_units = form.weather_units.data
        new_user.default_geocode = geocode_from_location_mq(form.default_location.data)
        db.session.add(new_user)
        db.session.commit()
        login_session(new_user)
        return redirect('/')

    return render_template('user-new.html', form=form)


@app.route('/users/<int:user_id>')
def return_user_profile(user_id):
    """Show user profile to anyone. Show user's default current weather location and most recent route to a logged in user viewing their own page. This is the user's landing page after logging in."""
    user = User.query.get_or_404(user_id)
    user.full_name = user.make_full_name()
    weather = current_weather_from_geocode((user.default_geocode_lat, user.default_geocode_lng))
    return render_template ('user.html', user=user, weather=weather)

@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user_profile(user_id):
    """Validate that logged in user is the one editing their own profile, turn away others. Load form to edit user profile."""
    if not g.user.id == user_id:
        flash('You can only edit your own profile.', 'danger')
        return redirect('/users')
    
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect (f'/users/{user.id}')
    
    return render_template('user-edit.html', user=user, form=form)

@app.route('/api/users/<int:user_id>', methods=["GET"])
def api_return_user_profile(user_id):
    """Returns user information via API call."""
    user = User.query.get_or_404(user_id)
    user_obj = {user_id: {}}
    user_obj[user_id]['username'] = user.username
    user_obj[user_id]['email'] = user.email
    user_obj[user_id]['first_name'] = user.first_name
    user_obj[user_id]['last_name'] = user.last_name
    user_obj[user_id]['profile_pic_image_url'] = user.profile_pic_image_url
    user_obj[user_id]['fav_bike'] = user.fav_bike
    user_obj[user_id]['bike_image_url'] = user.bike_image_url
    user_obj[user_id]['default_bike_type'] = user.default_bike_type
    user_obj[user_id]['default_geocode_lat'] = user.default_geocode_lat
    user_obj[user_id]['default_geocode_lng'] = user.default_geocode_lng
    user_obj[user_id]['weather_units'] = user.weather_units
    return jsonify(user_obj)

@app.route('/api/users/<int:user_id>/edit', methods=["PUT", "PATCH"])
def api_edit_user_profile():
    """Edit user profile, including preferences such as default route type, metric or imperial units, &c. Will also edit other aspects of a user profile such as bio, favorite bike, &c."""
    # TBH, I don't really see why this path is needed. I think I was going to do this from JS, but since I'm using Flask WTForms for the form, I'm not sure it's worth figuring out how to get that data to JS.


@app.route('/api/users/<int:user_id>/delete', methods=["DELETE"])
def delete_user(user_id):
    """Permanently deletes a user from the database using HTTP API call."""
    user = User.query.get_or_404(user_id)
    # does this need some kind of authorization and data verification logic???
    db.session.delete(user)
    db.session.commit()

@app.route('/login', methods=["GET", "POST"])
def login():
    """logs a user in"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user: 
            login_session(user)
            return redirect(f'/users/{user.id}')
        else:
            flash('those credentials did not match any known user', 'warning')
            return redirect ('/login')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """logs a user out"""
    if CURR_USER in session:
        flash (f'you have logged out', 'success')
        logout_session()
        
    return redirect('/')

########################
##### route routes #####
########################
@app.route('/api/routes/preview', methods=["GET"])
def preview_route():
    """Returns a route or choices of routes. Commented-out code will be for future development, but for now the routes all come from the Mapbox API. 
    Accepts coordinates grouped in checkpoints (latitude and longitude need to be grouped by checkpoint, but checkpoints come with numbers and do not need to be in order.
    Also will accept profile type, defaults to "regular" (which is translated to "cycle" for mapbox)
    """
    
    requests_dic = parse_geocode(request.args.to_dict())
    # profile = ""
    # if "profile" in requests_dic:
    #     profile = requests_dic.profile

    try:
        geostring = parse_geocode(requests_dic)
    except: 
        error = {"Errors": {"garbage error": "Garbage in, garbage out. Look at your URL."}}
        return 
    if type(geostring) == dict:
        return jsonify({"errors": geostring})
    
    errors_object = {}

    # for future development using ORS directions
    # try:
    #     return {"ORS": jsonify(ORS_directions(geoarray, profile))}
    # except:
    #     errors_object['ORS error'] = f'ORS_directions in helpers.py is not responding to these coordinates: {geoarray}'
    try:
        return {"mapbox": jsonify(mapbox_directions(geostring)), "errors": errors_object}
    except:
        # at the moment, these error messages are written for development
        errors_object['mapbox error'] = f'mapbox_directions in helpers.py is not responding to these coordinates: {geostring}'
    
    # if we're here, both have failed and errors_object should be returned
    return {"errors": errors_object}

@app.route('/api/routes/new', methods=["GET","POST"])
def create_new_route():
    """Gather route information. 
    With GET the raw data comes from the query string and is sent to the Mapbox API. 
    POST saves new route to database. 
    Will save to a guest user if there's no logged-in user. 
    For actual production, this would only be availble to logged-in users, but for portfolio it will work for anyone.
    """
    if request.method == 'GET':
        cps = request.args['cps'] or False
        coordinates = ""
        success = False
        errors = False
        troubleshooting = False
        try: 
            for i in range((int(cps)+1)):
                lng = request.args[f'{int(i)}-lng'] or i
                lat = request.args[f'{int(i)}-lat'] or i
                if i > 0:
                    coordinates = coordinates + ';'
                coordinates = coordinates + f'{lng},{lat}'
            # error is happening in mapbox_directions, 'sfar as I can tell
            
            success = mapbox_directions(coordinates)
        except: 
            errors = {"api error": "route API failed"}
            troubleshooting = {"troubleshooting": {"cps": cps, "coordinates": coordinates}}
        if success:
            ret_dic = success
        else: 
            ret_dic = {}
            if errors:
                ret_dic["errors"] = errors
            if troubleshooting:
                ret_dic["troubleshooting"] = troubleshooting
        
        return ret_dic
        
    else:
        return "POST"


@app.route('/routes/new')
def process_new_route_form():
    """render the RouteForm, applying query string data to pre-populate the forms including the number of checkpoint forms and the order in which they appear"""

    # something is breaking Ashir's 'puter when the template loads.... 
    # might be this cps thing...?
    # but I doubt it...

    cps = int(request.args.get('cps')) if request.args.get('cps') else 0
    lats = []
    lngs = []
    locations = []
    locations_values = []
    for i in range(int(cps)+1):
        if request.args.get(f'{i}-lat'):
            lats.append(float(request.args.get(f'{i}-lat')))
        else:
            lats.append(False)
        if request.args.get(f'{i}-lat'):
            lngs.append(float(request.args.get(f'{i}-lng')))
        else:
            lngs.append(False)
        locations.append(location_from_geocode_mb(lats[i], lngs[i]))
        locations_values.append(string_from_geocode([lats[i], lngs[i]]))
    
    if request.args.get('999-lat'):
        lats.append(float(request.args.get('999-lat')))
    else:
        lats.append(False)
    if request.args.get('999-lat'):
        lngs.append(float(request.args.get('999-lng')))
    else:
        lngs.append(False)
    locations.append(location_from_geocode_mb(lats[cps+1], lngs[cps+1]))
    locations_values.append(string_from_geocode([lats[cps+1], lngs[cps+1]]))

    route_form = RouteForm()
    # start_form = NewCheckpointForm(prefix="cp-0")
    # end_form = NewCheckpointForm(prefix="cp-999")
    # additional_forms = []
    # for i in range(cps):
    #     additional_forms.append(NewCheckpointForm(prefix=f"cp-{i}"))
    
    # start_form=start_form, end_form=end_form, additional_forms=additional_forms, 
    return render_template ('route-ors.html', cps=cps, route_form=route_form, lats=lats, lngs=lngs, locations=locations, locations_values=locations_values)

@app.route('/api/routes')
def display_available_routes():
    """Return a list of available routes sorted from most to least recent update. Guest users see one list of all publicly-available routes. Logged in users see their own routes in one list followed by all other public routes in a second list."""

# @app.route('/api/routes')
# def display_users_routes():
#     """Show route on map and with step-by-step directions, and weather information for the route. This uses the GET method to store all route information in the query string."""

@app.route('/api/routes/<id>')
def display_saved_route():
    """Build the query string from a saved route and redirect to '/route'. This can be accessed by any user, or by a guest who is not logged in."""

@app.route('/api/routes/<id>/edit')
def edit_saved_route():
    """The user who created a route can edit their route here. Any other user (or guest) can create a new route using this one as a strating point."""

#############################
##### checkpoint routes #####
#############################
@app.route('/checkpoint/new', methods=["GET", "POST"])
def create_new_checkpoint():
    """Creates a new checkpoint places it within a route"""

@app.route('/api/geocode')
def get_geocode_for_location():
    """returns geocode for an input location as a list of [latitude, longitude]"""
    # if 
    # location = request.args['location']

    # return lat, lng
    

###### might need following code for checkpoint routes
        # end_geoloc=geocode_from_location_mq(form.end_location.data)
        # if not start_geoloc or not end_geoloc:
        #     if start_geoloc:
        #         flash('The ending location could not be located. Please try again.', 'warning')
        #     elif end_geoloc:
        #         flash('The starting location could not be located. Please try again.', 'warning')
        #     else:
        #         flash('Neither of those locations could be located. Please try again')
        #     return render('route-ors.html', form=form)


        # if len(start_geoloc) > 1 or len(end_geoloc) > 1:
        #     flash("Hey, Tor. There's more than one valid response and you haven't written the code to chose which one is right.")

########################
##### error routes #####
########################
@app.errorhandler(404)
def display_404_message(err):
    """Display error message for 404."""
    if request.path.startswith('/users/'):
        return render_template('users/404.html'), 404
    if request.path.startswith('/routes/'):
        return render_template('routes/404.html'), 404
    return render_template('404.html'), 404



