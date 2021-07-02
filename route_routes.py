from app import app
from flask import Flask, flash, render_template, redirect
# , jsonify, session, g
from helpers import CURR_USER, CURR_ROUTE, CURR_CHECKPOINT_LIST, GUEST
from api import geocode_from_location, current_weather_from_geocode
from forms import NewRouteForm, NewCheckpointForm
from models import db, Route
import requests
from datetime import datetime


@app.route('/api/routes/new', methods=["POST"])
def create_new_route():
    """Create a new route from AJAX/Axios API call from `routes.js`"""



@app.route('/routes/new')
def process_new_route_form():
    route_form = NewRouteForm()
    start_form = NewCheckpointForm()
    end_form = NewCheckpointForm()

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
        
    return render_template ('new-route.html', route_form=route_form, start_form=start_form, end_form=end_form)

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

