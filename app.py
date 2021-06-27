import os

from flask import Flask, request, redirect, render_template, flash, jsonify, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User, Route, Checkpoint
from forms import NewRouteForm
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

from routes import weather_routes
# , user_routes, route_routes, 

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
    """Loads home page.
    If there is a logged in user, page shows weather from user's default location and most recently created route.
    If no one is logged in, page shows weather from default location (Albuquerque, NM because that's my joint) in metric units (because cycling). Offer the user option to change the location (including to their browser's location) and the units. (Location change handled in app.js; units change handled hear)
    """
    # city = ""
    if not request.method == "POST":
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
        location = request.data.location
        units = request.data.unitSelect
        
    # weather_prefs_form = WeatherPrefsForm()
    # if weather_prefs_form.validate_on_submit():
    #     location=form.data.location
    #     units=form.data.units

    geocode_list=geocode_from_location(location)
    if len(geocode_list) == 0:
        flash('Geocoding error: no results found for location.', 'warning')
        return redirect('/')
    if len(geocode_list) > 1:
        return render_template('geocode-choices.html', geocode_list=geocode_list, return_to='/')
    geocode = geocode_list[0]

    # (city, conditions, weather_icon_url, current_weather_details) = current_weather_from_geocode(geocode, units)
    weather = current_weather_from_geocode(geocode)
    # print (f'----------------{weather}')
    # 
    # -----------
    # {
        # 'city': 'Albuquerque', 
        # 'conditions': 'Scattered Clouds', 
        # 'weather_icon_url': 'http://openweathermap.org/img/wn/03d@2x.png', 
        # 'current_weather_details': {
            # 'Temperature': '31.83℃', 
            # 'Feels Like': '29.7℃', 
            # 'High': '34.02℃', 
            # 'Low': '29.87℃', 
            # 'Relative Humidity': '17%', 
            # 'Wind Speed': '3.13 km/h', 
            # 'Wind Direction': '315°'}}



    return render_template('home.html', weather=weather)

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

    