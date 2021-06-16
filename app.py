import os

from flask import Flask, request, redirect, render_template, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Route, Checkpoint
from forms import NewRouteForm
import requests
# from secrets import ORS_API_KEY, MQ_API_KEY
# from helpers import ORS_API_BASE_URL, MQ_API_BASE_URL
from helpers import geocode_from_location

from londons import londons_string_from_hell as londons

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///saddle_time_db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "really_fucking_secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def load_home_page():
    return render_template('home.html')

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

    