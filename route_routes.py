from app import app
from flask import Flask
from helpers import CURR_USER, CURR_ROUTE, CURR_CHECKPOINT_LIST, GUEST
from api import geocode_from_location, current_weather_from_geocode
from forms import NewRouteForm
# , jsonify, session, g
import requests


@app.route('api/routes/new', methods=["GET", "POST"])
def create_new_route():
    """Create a new route, including adding and re-arranging checkpoints."""
    form = NewRouteForm()
    
    if form.validate_on_submit():
        route_name = form.route_name.data or "untitled"
        start_geoloc=geocode_from_location(form.start_location.data)
        end_geoloc=geocode_from_location(form.end_location.data)
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

@app.route('/routes')
def display_public_routes():
    """Display a list of available routes sorted from most to least recent update. Guest users see one list of all publicly-available routes. Logged in users see their own routes in one list followed by all other public routes in a second list."""

@app.route('/api/routes')
def display_users_routes():
    """Show route on map and with step-by-step directions, and weather information for the route. This uses the GET method to store all route information in the query string."""

@app.route('/routes/save')
def save_route():
    """Save a route into the database. Page can only be accessed by registered and logged-in users."""

@app.route('/api/routes/<id>')
def display_saved_route():
    """Build the query string from a saved route and redirect to '/route'. This can be accessed by any user, or by a guest who is not logged in."""

@app.route('/api/routes/<id>/edit')
def edit_saved_route():
    """The user who created a route can edit their route here. Any other user (or guest) can create a new route using this one as a strating point."""

