import os

from flask import Flask, request, redirect, render_template, flash, jsonify, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User, Route, Checkpoint
from forms import NewRouteForm
from api import geocode_from_location, current_weather_from_geocode
from helpers import login_session, logout_session, CURR_USER, CURR_ROUTE, CURR_CHECKPOINT_LIST, GUEST


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///saddle_time_db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "really_very_secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# from routes import weather_routes, user_routes
# , route_routes, 
import weather_routes, user_routes
# , route_routes

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
    # city = ""
    if not request.method == "POST":
        try: 
            if g.user.id:
                return redirect(f'/users/{g.user.id}')
        except:
            flash ('logged in user does not have an id; this could be because it is a guest user', 'info')
        try:
            if g.user.location:
                location=g.user.location
            else:
                location="Albuquerque, NM 87102 USA"
        except:
            location="Albuquerque, NM 87102 USA"
        
        try:
            if g.user.weather_units:
                units=g.user.weather_units
            else:
                units="metric"
        except:
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

    return render_template('home.html', weather=weather)


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



