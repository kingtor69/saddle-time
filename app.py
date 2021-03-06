import os

from flask import Flask, request, redirect, render_template, flash, jsonify, session, g, Response
from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User, Route, Checkpoint
from forms import UserNewForm, UserEditForm, LoginForm
from helpers import *
from random import randrange

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///saddle_time_db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'really_very_secret')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.before_request
def add_user_to_g():
    """If user is logged in, add that user to `g`."""
    if CURR_USER in session:
        g.user = User.query.get(session[CURR_USER])

@app.route('/', methods=["GET"])
def load_home_page():
    """Loads home page.
    Page defaults to weather from default location (Coffee Shop in The Mission, San Francisco) in imperial units. Offers the user option to change the location and the units.
    """
    # default values: 
    location = DEFAULT_LOCATION
    loc_lat = DEFAULT_LOC_LAT
    loc_lng = DEFAULT_LOC_LNG
    units = DEFAULT_UNITS
    try:
        # or query string values
        if 'latitude' in request.args and 'longitute' in request.args:
            loc_lat = request.args['latitude']
            loc_lng = request.args['longitute']
        elif 'lat' in request.args and 'lng' in request.args:
            loc_lat = request.args['lat']
            loc_lng = request.args['lng']
        elif 'location' in request.args:
            location = request.args['location']
            [loc_lng, loc_lat] = geocode_from_location_mb(location)
        # or user default values
        elif g.user:
            loc_lat = g.user.default_geocode_lat
            loc_lng = g.user.default_geocode_lng
            location = location_from_geocode_mb(loc_lat, loc_lng)
    # tell user that defaults are being used
    except:
        flash(f'using default location ({DEFAULT_LOCATION_LOGICAL_NAME})', 'info')

    try: 
        # now see if units are in query string
        if 'units' in request.args:
            units = request.args['units']
        # or look in the logged-in user defaults
        elif g.user:
            units = g.user.units
    # tell user that default units being used
    except:
        flash('using default temperature and distance units (imperial)', 'info')

    weather = current_weather_from_geocode([loc_lat, loc_lng], units)

    return render_template('home.html', weather=weather, lng=loc_lng, lat=loc_lat, location=location, units=units)

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

@app.route('/api/geocode/reverse', methods=["GET"])
def location_from_geocode():
    try: 
        lat = request.args['lat']
        lng = request.args['lng']
        return jsonify(location_from_geocode_mb(lat, lng))
    except:
        return {"results": {"Errors": {"Geocoding error": "Invalid geocode data entered."}}}

@app.route('/api/weather', methods=["GET"])
def retrieve_weather_data_from_geocode():
    """gather weather data from units & geocode input
    NOTE: the geocode used by the weather API is lat-lng whereas mapbox uses lng-lat, and that's one reason this accepts latitude and longitude as separate arguments."""

    units = request.args['units']
    geocode = (request.args['lat'], request.args['lng'])
    return jsonify(current_weather_from_geocode(geocode, units))


#######################
##### user routes #####
#######################
@app.route('/users/signup', methods=["GET", "POST"])
def signup_new_user():
    """Sign up new users. Enter into database"""
    alt_destintation = request.args.get('route') if request.args.get('route') else False
    form = UserNewForm()
    if form.validate_on_submit():
        new_user = User.hashpass(form.username.data, form.password.data)
        new_user.email = form.email.data
        new_user.first_name = form.first_name.data
        new_user.last_name = form.last_name.data
        new_user.profile_pic_image_url = form.profile_pic_image_url.data if form.profile_pic_image_url.data else f"/static/images/{STOCK_PROFILE_PICS[randrange(0,(len(STOCK_PROFILE_PICS)-1))]}"
        new_user.fav_bike = form.fav_bike.data
        new_user.bike_image_url = form.bike_image_url.data if form.bike_image_url.data else f"/static/images/{STOCK_BIKE_PICS[randrange(0,(len(STOCK_BIKE_PICS)-1))]}"
        new_user.units = form.units.data
        new_user.default_geocode_lat = DEFAULT_LOC_LAT
        new_user.default_geocode_lng = DEFAULT_LOC_LNG
        db.session.add(new_user)
        db.session.commit()
        login_session(new_user)
        alt_destination = request.form.get('alt_destation')
        if alt_destination:
            return redirect(alt_destination)
        return redirect(f'/users/{new_user.id}')

    return render_template('user-new.html', form=form)

@app.route('/users')
def list_all_users():
    users = User.query.all()
    for user in users:
        user.full_name = user.make_full_name()
    return render_template('user-list.html', users=users)

@app.route('/users/<int:user_id>')
def return_user_profile(user_id):
    """Show user profile to anyone and allow user to edit or delete themself. This is also the user's landing page after logging in."""
    user = User.query.get_or_404(user_id)
    user.full_name = user.make_full_name()
    user_routes = Route.query.filter_by(user_id=user.id).all()
    num_routes = len(user_routes)
    is_logged_in_user = False
    if 'user' in g and g.user.id == user.id:
        is_logged_in_user = True

    return render_template ('user.html', user=user, routes=user_routes, num_routes = num_routes, is_logged_in_user=is_logged_in_user)

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
        user.profile_pic_image_url = form.profile_pic_image_url.data if form.profile_pic_image_url.data else f"/static/images/{STOCK_PROFILE_PICS[randrange(0,(len(STOCK_PROFILE_PICS)-1))]}"
        user.profile_pic_image_url = form.profile_pic_image_url.data if form.profile_pic_image_url.data else f"/static/images/{STOCK_PROFILE_PICS[randrange(0,(len(STOCK_PROFILE_PICS)-1))]}"

        db.session.add(user)
        db.session.commit()
        return redirect (f'/users/{user.id}')
    
    return render_template('user-edit.html', user=user, form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """logs a user in"""
    alt_destination = request.args.get('return') if request.args.get('return') else False
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        alt_destination = request.form.get('alt_destination')
        try:
            login_session(user)
            if alt_destination:
                return redirect(alt_destination)
            return redirect(f'/users/{user.id}')
        except:
            flash('those credentials did not match any known user', 'warning')
            return redirect ('/login')
    return render_template('login.html', form=form, alt_destination=alt_destination)

@app.route('/logout')
def logout():
    """logs a user out"""
    if not request.args.get('deleted'):
        flash (f'you have logged out', 'success')
    if CURR_USER in session:
        logout_session()
        
    return redirect('/')

########################
##### route routes #####
########################
@app.route('/route')
def prepare_new_route():
    """display existing route, edit or prepare new route, applying query string data to pre-populate the forms including the number of checkpoint forms and the order in which they appear"""

    # cps is the number of additional checkpoints
    cps = int(request.args.get('cps')) if request.args.get('cps') else 0
    new_cp_id = int(request.args['new-id']) if request.args.get('new-id') else -1
    lats = []
    lngs = []
    locations = []
    locations_values = []
    cp = 0
    for i in range(int(cps)+1):
        if i == new_cp_id:
            lats.append(False)
            lngs.append(False)
            locations.append(False)
        else:
            if request.args.get(f'{cp}-lat'):
                lats.append(float(request.args.get(f'{cp}-lat')))
            else:
                lats.append(False)
            if request.args.get(f'{cp}-lat'):
                lngs.append(float(request.args.get(f'{cp}-lng')))
            else:
                lngs.append(False)
            locations.append(location_from_geocode_mb(lats[i], lngs[i]))
            locations_values.append(string_from_geocode([lats[i], lngs[i]]))
            cp += 1
    
    if request.args.get('999-lat'):
        lats.append(float(request.args.get('999-lat')))
    else:
        lats.append(False)
    if request.args.get('999-lng'):
        lngs.append(float(request.args.get('999-lng')))
    else:
        lngs.append(False)
    locations.append(location_from_geocode_mb(lats[cps+1], lngs[cps+1]))
    locations_values.append(string_from_geocode([lats[cps+1], lngs[cps+1]]))

    return render_template ('route.html', cps=cps, new_cp_id=new_cp_id, lats=lats, lngs=lngs, locations=locations, locations_values=locations_values)

    return render_template ('route.html', cps=cps, new_cp_id=new_cp_id, lats=lats, lngs=lngs, locations=locations, locations_values=locations_values)

###########################
##### user API routes #####
###########################
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
    user_obj[user_id]['units'] = user.units
    return jsonify(user_obj)

@app.route('/api/users/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    """Permanently deletes a user from the database using HTTP API call."""
    if g.user.id == user_id:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"delete": "confirmed"})
    return jsonify({"Errors": {"danger": "Only a logged-in user can delete themself."}})

############################
##### route API routes #####
############################
@app.route('/api/routes/preview', methods=["GET"])
def preview_route():
    """Returns a route or choices of routes. 
    Accepts coordinates grouped in checkpoints (latitude and longitude need to be grouped by checkpoint, but checkpoints come with numbers and do not need to be in order.
    """
    try:
        geostring = parse_geocode(request.args.to_dict())
    except: 
        return jsonify({"Errors": {"Invalid data": "Unable to parse geocode data."}})
    if type(geostring) == dict:
        return jsonify({"Errors": geostring})
    try:
        directions = mapbox_directions(geostring)
        directions_plus_elevations = mapquest_elevation(directions)
        return jsonify(directions_plus_elevations)
    except:
        return jsonify({"Errors": {"Invalid data": "Some of the data submitted is invalid."}})


@app.route('/api/routes/new')
def create_new_route():
    """Gather route information. 
    """
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
        
        success = mapbox_directions(coordinates)
    except: 
        errors = {"api error": "route API failed"}
        troubleshooting = {"troubleshooting": {"cps": cps, "coordinates": coordinates}}
    if success:
        ret_dic = success
    else: 
        ret_dic = {}
        if errors:
            ret_dic["Errors"] = errors
        if troubleshooting:
            ret_dic["troubleshooting"] = troubleshooting
    
    return ret_dic
        
@app.route('/api/routes')
def display_available_routes():
    """GET returns a list of available routes sorted from most to least recent update.
    """
    routes = Route.query.all()
    return render_template('routes.html', routes=routes)
 
@app.route('/api/routes', methods=["POST"])
def save_new_route():
    """POST saves a new route to the database,
    along with all checkpoints used in that route,
    and the checkpoints-routes many-to-many table.
    """
    errors = {'Errors': {}}
    missing_data_errors = []
    new_checkpoints = []
    new_checkpoints_routes = []
    if not request.json:
        errors['Errors']['JSON error'] = 'requests must be of type application/json'
    elif not 'route' in request.json or not 'checkpoints' in request.json:
        if not 'route' in request.json:
            missing_data_errors.append["No route data found."]
        if not 'checkpoints' in request.json:
            missing_data_errors.append["No checkpoint data found."]

    if not 'user_id' in request.json['route']:
        missing_data_errors.append("User ID is required to create a new route.")
    if len(request.json['checkpoints']) < 2:
        missing_data_errors.append("Must have 2 or more checkpoints to save a route.")
    if len(missing_data_errors) > 0:
        errors['Errors']['missing data errors'] = missing_data_errors
    code = 418 if is_today_april_fools() else 400
    if errors['Errors']:
        return jsonify(errors, code)
    
    new_route = Route(user_id = request.json['route']['user_id'])
    if 'route_name' in request.json['route']:
        new_route.route_name = request.json['route']['route_name']
    if 'bike_type' in request.json['route']:
        new_route.bike_type = request.json['route']['bike_type']
    db.session.add(new_route)
    db.session.commit()

    try:
        for cp in request.json['checkpoints']:
            new_checkpoint = Checkpoint(
                checkpoint_lat = cp['lat'],
                checkpoint_lng = cp['lng']
            )
            if 'checkpoint_name' in cp:
                new_checkpoint.checkpoint_name = cp['checkpoint_name']
            new_checkpoints.append(new_checkpoint)
        db.session.add_all(new_checkpoints)
        db.session.commit()
    except:
        errors['Errors']['checkpoint error'] = "One or more checkpoints failed to save. Please check the saved route before you trust it's what you meant to save."

    try: 
        for i in range(len(new_checkpoints)):
            new_cpr = CheckpointRoute(
                route_id = new_route.id,
                checkpoint_id = new_checkpoints[i].id,
                route_order = i
            )
            new_checkpoints_routes.append(new_cpr)
        db.session.add_all(new_checkpoints_routes)
        db.session.commit()
    except:
        errors['Errors']['checkpoint-routing error'] = "One or more of the checkpoints failed to be saved in the correct order. Please check the saved route before you trust it's what you meant to save."
    
    serialized_route = new_route.serialize()
    serialized_checkpoints = []
    serialized_cprs = []
    for cp in new_checkpoints:
        serialized_checkpoints.append(cp.serialize())
    for cpr in new_checkpoints_routes:
        serialized_cprs.append(cpr.serialize())

    return (jsonify({
        'route': serialized_route,
        'checkpoints': serialized_checkpoints,
        'checkpoints-routes': serialized_cprs
    }), 201)

@app.route('/api/routes/<int:id>', methods=["GET"])
def retrieve_saved_route(id):
    """Gather all data for a route (includes checkpoints and checkpoints_routes). This can be accessed by any user, or by a guest who is not logged in."""
    route_orm = Route.query.get_or_404(id)
    route = {
        'id': route_orm.id,
        'route_name': route_orm.route_name,
        'user_id': route_orm.user_id
    }
    try:
        cprs = CheckpointRoute.query.filter_by(route_id=id).all()
        last_i = len(cprs)-1
        for i in range(len(cprs)):
            cp = Checkpoint.query.get(cprs[i].checkpoint_id)
            if not(i == last_i):
                lat_key = f'{cprs[i].route_order}-lat'
                lng_key = f'{cprs[i].route_order}-lng'
            else:
                lat_key = '999-lat'
                lng_key = '999-lng'
            route[lat_key] = cp.checkpoint_lat
            route[lng_key] = cp.checkpoint_lng
    except: 
        return (jsonify({"Errors": {"retrieval error": f"Something went wrong retrieving route #{id}"}}), 500)

    return (jsonify({"route": route}), 200)

@app.route('/api/routes/<int:id>', methods=["DELETE"])
def delete_route(id):
    route_to_delete = Route.query.get_or_404(id)
    if not route_to_delete.user_id == g.user.id:
        return {"Errors": {"authentication error": "only the user who created a route can delete it"}}
    try:
        db.session.delete(route_to_delete)
        db.session.commit()
    except:
        return (jsonify({"Errors": {"delete error": f"unable to delete route #{id}"}}), 500)

    return (jsonify({"delete": f"delete route #{id} confirmed"}), 200)

@app.route('/api/routes/<int:id>', methods=["PATCH"])
def edit_saved_route(id):
    """The user who created a route can edit their route here. Requires authentication."""
    errors = {'Errors': {}}
    missing_data_errors = []
    new_checkpoints = []
    new_checkpoints_routes = []
    if not request.json:
        errors['Errors']['JSON error'] = 'requests must be of type application/json'
    elif not 'route' in request.json or not 'checkpoints' in request.json:
        if not 'route' in request.json:
            missing_data_errors.append["No route data found."]
        if not 'checkpoints' in request.json:
            missing_data_errors.append["No checkpoint data found."]
        else:
            checkpoints_array = request.json['checkpoints']

    if not 'user_id' in request.json['route']:
        missing_data_errors.append("User ID is required to create a new route.")
    if len(request.json['checkpoints']) < 2:
        missing_data_errors.append("Must have 2 or more checkpoints to save a route.")
    if len(missing_data_errors) > 0:
        errors['Errors']['missing data errors'] = missing_data_errors
    code = 418 if is_today_april_fools() else 400
    if errors['Errors']:
        return jsonify(errors, code)
    
    route_to_patch = Route.query.get_or_404(id)
    if 'route_name' in request.json['route']:
        route_to_patch.route_name = request.json['route']['route_name']
    if 'bike_type' in request.json['route']:
        route_to_patch.bike_type = request.json['route']['bike_type']

    db.session.commit()

    cprs_obsolete = CheckpointRoute.query.filter_by(route_id = id)

    for cpr in cprs_obsolete:
        cp = Checkpoint.query.filter_by(id = cpr.checkpoint_id).first()
        db.session.delete(cp)
        db.session.delete(cpr)
    try:
        for cp in request.json['checkpoints']:
            new_checkpoint = Checkpoint(
                checkpoint_lat = cp['lat'],
                checkpoint_lng = cp['lng']
            )
            if 'checkpoint_name' in cp:
                new_checkpoint.checkpoint_name = cp['checkpoint_name']
            new_checkpoints.append(new_checkpoint)
        db.session.add_all(new_checkpoints)
        db.session.commit()
    except:
        errors['Errors']['checkpoint error'] = "One or more checkpoints failed to save. Please check the saved route before you trust it's what you meant to save."

    try: 
        for i in range(len(new_checkpoints)):
            new_cpr = CheckpointRoute(
                route_id = route_to_patch.id,
                checkpoint_id = new_checkpoints[i].id,
                route_order = i
            )
            new_checkpoints_routes.append(new_cpr)
        db.session.add_all(new_checkpoints_routes)
        db.session.commit()
    except:
        errors['Errors']['checkpoint-routing error'] = "One or more of the checkpoints failed to be saved in the correct order. Please check the saved route before you trust it's what you meant to save."
    
    serialized_route = route_to_patch.serialize()
    serialized_checkpoints = []
    serialized_cprs = []
    for cp in new_checkpoints:
        serialized_checkpoints.append(cp.serialize())
    for cpr in new_checkpoints_routes:
        serialized_cprs.append(cpr.serialize())

    code = 418 if is_today_april_fools() else 400
    if errors['Errors']:
        return jsonify(errors['Errors'], code)

    return (jsonify({
        'route': serialized_route,
        'checkpoints': serialized_checkpoints,
        'checkpoints-routes': serialized_cprs
    }), 201)


#############################
##### checkpoint routes #####
#############################
@app.route('/api/checkpoints')
def display_users_checkpoints():
    """Returns list of logged-in user's checkpoints."""

@app.route('/api/checkpoints', methods=["POST"])
def create_new_checkpoint():
    checkpoint_name = ''
    if 'checkpoint_name' in request.json:
        checkpoint_name = request.json['checkpoint_display_name']
    new_checkpoint = Checkpoint(
        user_id=request.json['user_id'],
        checkpoint_display_name=checkpoint_name,
        checkpoint_lat=request.json['lat'],
        checkpoint_lng=request.json['lng']
    )

    db.session.add(new_checkpoint)
    db.session.commit()

    return (jsonify(checkpoint=new_checkpoint.serialize()), 201)
    
@app.route('/api/checkpoints/<int:checkpoint_id>')
def display_specific_checkpoint():
    """Returns geocode for a checkpoint selected by ID."""

@app.route('/api/checkpoints/<int:checkpoint_id>/edit')
def edit_checkpoint():
    """Allows logged in user to edit their checkpoints."""

#######################################
#### checkpoints-routes m2m routes ####
#######################################
@app.route('/api/checkpoints-routes', methods=["POST"])
def create_new_m2m_checkpoint_route():
    new_checkpoint_route = CheckpointRoute(
        route_id=request.json['route_id'],
        checkpoint_id=request.json['checkpoint_id'],
        route_order=request.json['route_order']
    )
    db.session.add(new_checkpoint_route)
    db.session.commit()
    
    return (jsonify(checkpoint_route=new_checkpoint_route.serialize()), 201)

########################
##### error routes #####
########################
@app.errorhandler(404)
def display_404_message(err):
    """Display error message for 404."""
    if request.path.startswith('/users/'):
        return render_template('users/404.html'), 404
    if request.path.startswith('/route/'):
        return render_template('routes/404.html'), 404
    return render_template('404.html'), 404
