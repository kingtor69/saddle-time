import os

from flask import Flask, request, redirect, render_template, flash, jsonify, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User, Route, Checkpoint
from forms import NewRouteForm, NewUserForm, LoginForm, NewCheckpointForm
from helpers import login_session, logout_session, CURR_USER, CURR_ROUTE, CURR_CHECKPOINT_LIST, GUEST, geocode_from_location, current_weather_from_geocode

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




@app.route('/', methods=["GET", "POST"])
def load_home_page():
    """Loads home page.
    If there is a logged in user, page shows weather from user's default location and most recently created route.
    If no one is logged in, page shows weather from default location (Albuquerque, NM because that's my joint) in metric units (because cycling). Offer the user option to change the location (including to their browser's location) and the units. (Location change handled in app.js; units change handled hear)
    """
    location = ""
    if not request.method == "POST":
        try:
            location = g.user.location if g.user.location else "949 Montoya St NW, Albuquerque, NM 87104"
        except:
            flash('using default location (Bike in Coffee in old town Albuquerque, NM)', 'info')
            location="949 Montoya St NW, Albuquerque, NM 87104"
        
        try:
            units=g.user.weather_units if g.user.weather_units else "metric"
        except:
            flash('using default measurement units (metric)', 'info')
            units="metric"
    else:
        # in other words, request.method IS "POST"
        location = request.location.data
        units = request.unitSelect.data
        
    # weather_prefs_form = WeatherPrefsForm()
    # if weather_prefs_form.validate_on_submit():
    #     location=form.location.data
    #     units=form.units.data

    geocode_list=geocode_from_location(location)
    if len(geocode_list) == 0:
        flash('Geocoding error: no results found for location.', 'warning')
        return redirect('/')
    if len(geocode_list) > 1:
        return render_template('geocode-choices.html', geocode_list=geocode_list, return_to='/')
    geocode = geocode_list[0]

    weather = current_weather_from_geocode(geocode)

    return render_template('home.html', weather=weather, lng=geocode[1], lat=geocode[0])


##########################
##### weather routes #####
##########################
@app.route('/api/weather', methods=["GET"])
def retrieve_weater_data():
    """collect and return weather information"""
    location = request.args['location'] or 'undefined'
    units = request.args['units'] or 'metric'
    geocode = request.args['geocode'] or 'undefined'
    errors = {"Errors": {}}
    error_count = 0
    if location == "undefined":
        errors["Errors"]["Location Error"] = "No valid location entered."
        error_count += 1
    if geocode == "undefined":
        errors["Errors"]["Geocoding Error"] = "No valid geocode entered."
        error_count += 1
        geocode_list=geocode_from_location(location)
        if len(geocode_list) == 0:
            errors["Errors"]["Geocoding Error"] = "No Results Found For Location"
            error_count += 1
        if len(geocode_list) > 1:
            errors["Errors"]["Geocoging Error"] = "More than one result. Please be more specific."
            error_count += 1
        geocode = geocode_list[0]

    if error_count > 1:
        return jsonify(errors)

    return jsonify(current_weather_from_geocode(geocode, units))


#######################
##### user routes #####
#######################

@app.route('/users/signup', methods=["GET", "POST"])
def signup_new_user():
    """Sign up new users. Enter into database"""

    form = NewUserForm()
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
        new_user.default_geocode = geocode_from_location(form.default_location.data)
        db.session.add(new_user)
        db.session.commit()
        login_session(new_user)
        return redirect('/')

    return render_template('new-user.html', form=form)


@app.route('/users/<int:user_id>')
def show_user_profile(user_id):
    """Show user profile to anyone. Show user's default current weather location and most recent route to a logged in user viewing their own page. This is the user's landing page after logging in."""
    user = User.query.get_or_404(user_id)
    user.full_name = user.make_full_name()
    return render_template ('user.html', user=user)


@app.route('/api/users/<user_id>/edit', methods=["PUT", "PATCH"])
def edit_user_profile():
    """Edit user profile, including preferences such as default route type, metric or imperial units, &c. Will also edit other aspects of a user profile such as bio, favorite bike, &c."""

@app.route('/api/users/<user_id>/delete', methods=["DELETE"])
def delete_user():
    """Permanently deletes a user from the database using HTTP API call."""

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
        logging_out_user = g.user.username
        flash (f'{logging_out_user} successfully logged out', 'success')
        logout_session()
        
    return redirect('/')

########################
##### route routes #####
########################
@app.route('/api/routes/new', methods=["POST"])
def create_new_route():
    """Create a new route from AJAX/Axios API call from `routes.js`"""

@app.route('/routes/new')
def process_new_route_form():
    """render the new-route form, applying query string data to pre-populate the forms including the number of checkpoint forms and the order in which they appear"""

    cps = int(request.args.get('cps')) if request.args.get('cps') else 0
    route_form = NewRouteForm()
    start_form = NewCheckpointForm(prefix="cp-0")
    end_form = NewCheckpointForm(prefix="cp-999")
    additional_forms = []
    for i in range(1, cps):
        additional_forms.append(NewCheckpointForm(prefix=f"cp-{i}"))
    

    
    # I think processing the form data is going to be better in JS
    # if you change your mind, you'll need this:
    # , methods=["GET", "POST"]
    # and this (and then some):
    # if route_form.validate_on_submit():
    #     route_name = form.route_name.data or "untitled"
    #     bike_type=form.bike_type.data
    #     timestamp = datetime.utcnow()

    #     user_id = 0;
    #     if not g.user.username == "guest":
    #         user_id = g.user.id
    #     new_route = Route(route_name=route_name, bike_type=bike_type, timestamp=timestamp, user_id=user_id)

    #     db.session.add(new_route)
    #     db.session.commit()
    #     return render_template('route.html', route=new_route)
        
    return render_template ('new-route.html', route_form=route_form, start_form=start_form, end_form=end_form, additional_forms=additional_forms)

@app.route('/api/routes')
def display_available_routes():
    """Return a list of available routes sorted from most to least recent update. Guest users see one list of all publicly-available routes. Logged in users see their own routes in one list followed by all other public routes in a second list."""

# @app.route('/api/routes')
# def display_users_routes():
#     """Show route on map and with step-by-step directions, and weather information for the route. This uses the GET method to store all route information in the query string."""

@app.route('/routes/save')
def save_route():
    """Save a route into the database. Page can only be accessed by registered and logged-in users."""

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
    """returns geocode for an input location from a list of [lattitude, longitude]"""
    

###### might need following code for checkpoint routes
        # end_geoloc=geocode_from_location(form.end_location.data)
        # if not start_geoloc or not end_geoloc:
        #     if start_geoloc:
        #         flash('The ending location could not be located. Please try again.', 'warning')
        #     elif end_geoloc:
        #         flash('The starting location could not be located. Please try again.', 'warning')
        #     else:
        #         flash('Neither of those locations could be located. Please try again')
        #     return render('new-route.html', form=form)


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



