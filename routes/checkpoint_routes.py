# from app import app
from flask import Flask, flash, Blueprint, render_template
# , jsonify, session, g
from helpers import CURR_USER, CURR_ROUTE, CURR_CHECKPOINT_LIST, GUEST, geocode_from_location, current_weather_from_geocode
from forms import NewRouteForm
import requests


checkpoint_routes = Blueprint("checkpoint_routes", __name__, static_folder="../static", template_folder="../templates")

############ this might all happen in JS.... not sure yet

@checkpoint_routes.route('/checkpoint/new', methods=["GET", "POST"])
def create_new_checkpoint():
    """Creates a new checkpoint places it within a route"""

@checkpoint_routes.route('/api/geocode')
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

