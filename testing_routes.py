import os
from flask import Flask, request, render_template, redirect
from models import db

os.environ['DATABASE_URL'] = "postgresql:///saddle_time_test_db"

from app import app

#######################################
##### routes for development only #####
#####    delete on deployment     #####
#######################################

@app.route('/home_test', methods=["POST"])
def test_home_page():
    """Home page test with test in POST route."""
    import pdb
    pdb.set_trace()
    weather={}
    weather['city'] = request.city.data
    weather['conditions'] = request.conditions.data
    weather['weather_icon_url'] = request.weather_icon_url.data
    weather['current_weather_details'] = {}
    current_weather_details_obj = request.current_weather_details.data


    weather['current_weather_details']['Temperature'] = current_weather_details_obj['Temperature']
    weather['current_weather_details']['High'] = current_weather_details_obj['High']
    weather['current_weather_details']['Low'] = current_weather_details_obj['Low']
    weather['current_weather_details']['Feels Like'] = current_weather_details_obj['Feels Like']
    weather['current_weather_details']['Relative Humidity'] = current_weather_details_obj['Relative Humidity']
    weather['current_weather_details']['Wind Speed'] = current_weather_details_obj['Wind Speed']
    weather['current_weather_details']['Wind Direction'] = current_weather_details_obj['Wind Direction']

    return render_template('home.html', weather=weather)

@app.route('/pdb', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def pdb_set_trace():
    """defined this route for debugging purposes"""
    import pdb
    pdb.set_trace()
    return redirect('/')

