import os

from flask import Flask, request, redirect, render_template, flash, jsonify, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User, Route, Checkpoint
from forms import NewRouteForm, WeatherPrefsForm
from api import geocode_from_location, current_weather_from_geocode

CURR_USER = "logged_in_user"
CURR_ROUTE = "route_in_progress"
CURR_CHECKPOINT_LIST = "checkpoints_in_use"
GUEST = User(username="guest", password="fakepassword")

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///saddle_time_db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "really_fucking_secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

from routes import user_routes, route_routes

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


def loginSession(user):
    """Log in a registered user to session."""

    session[CURR_USER] = user.id

def logoutSession():
    """Remove user who is logging out from session."""

    del session[CURR_USER]


@app.route('/', methods=["GET", "POST"])
def load_home_page():
    """loads home page.
    If there is a logged in user, page shows weather from user's default location and most recently created route.
    If no one is logged in, page shows weather from location data provided by browser or if blocked asks user for city to start off.
    """
    try:
        location=g.user.location
    except:
        location="Albuquerque, NM 87102 USA"
        
    try:
        units=g.user.weather_units
    except:
        units="metric"
        
    weather_prefs_form = WeatherPrefsForm()
    if weather_prefs_form.validate_on_submit():
        location=form.data.location
        units=form.data.units

    try:
        geocode = g.user.geocode
    except:
        geocode_list=geocode_from_location(location)
        if len(geocode_list) == 0:
            flash('Geocoding error: no results found for location.', 'warning')
            return redirect('/')
        if len(geocode_list) > 1:
            return render_template('geocode-choices.html', geocode_list=geocode_list, return_to='/')
        geocode = geocode_list[0]
    (city, conditions, weather_icon_url, current_weather_details) = current_weather_from_geocode(geocode, units)
    return render_template('home.html', city=city, conditions=conditions, weather_icon_url=weather_icon_url, current_weather_details=current_weather_details, form=weather_prefs_form)

@app.route('/routes/new', methods=['GET', 'POST'])
def make_new_route():
    form = NewRouteForm()
    
    if form.validate_on_submit():
        route_name = form.data.route_name or "untitled"
        start_geoloc=geocode_from_location(form.data.start_location)
        end_geoloc=geocode_from_location(form.data.end_location)
        if not start_geoloc or not end_geoloc:
            if start_geoloc:
                flash('The ending location could not be located. Please try again.', 'warning')
            elif end_geoloc:
                flash('The starting location could not be located. Please try again.', 'warning')
            else:
                flash('Neither of those locations could be located. Please try again')
            return render('new-route.html', form=form)
        if len(start_geoloc) > 1 or len(end_geoloc) > 1:
            flash("Hey, Tor. There's more than one valid response and you haven't written the code to chose which one is right.")
        new_route = Route(route_name=route_name, start=start_geoloc, end=end_geoloc)
        db.session.add(new_route)
        db.session.commit()
        return render_template('route.html', route=new_route)
        
    return render('new-route.html', form=form)

    