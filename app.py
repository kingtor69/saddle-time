from flask import FLask, request, redirect, render_template, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
import requests
from secrets import ORS_API_KEY
ORS_API_BASE_URL = "https://api.openrouteservice.org/v2/directions/"
MQ_API_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/"

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bike_friendly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "really_fucking_secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)