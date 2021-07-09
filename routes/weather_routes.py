# from app import app
from flask import Flask, request, Blueprint, render_template, redirect, flash, jsonify
# , session, g
# import requests
from helpers import geocode_from_location, current_weather_from_geocode

from flask import Blueprint, render_template

weather_routes = Blueprint("weather_routes", __name__, static_folder="../static", template_folder="../templates")

@weather_routes.route('/api/weather', methods=["GET"])
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