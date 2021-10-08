import os
from unittest import TestCase
from flask import jsonify
from helpers import *
import requests

from app import app


##############################
##### external API calls #####
##############################
class MapboxGeocodeAPITestCase(TestCase):
    """test mapbox geocoding API calls, forward and reverse"""
    def test_mapbox_geocode_forward(self):
        """test forward geocoding (retrieve coordinates from location)"""


    def test_mapbox_geocode_reverse(self):
        """test reverse geocoding (retrieve location from coordinates)"""
        good_geocode = "-106.582998,35.191097"
        bad_geocode = "35.191097,-106.582998"
        good_resp = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{good_geocode}.json?access_token={MB_API_KEY}')
        bad_resp = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{bad_geocode}.json?access_token={MB_API_KEY}')
        self.assertEqual(good_resp.status_code, 200)
        self.assertIn("features", good_resp.json())
        self.assertGreater(len(good_resp.json()["features"]), 0)
        self.assertEqual(bad_resp.status_code, 200)
        self.assertEqual(len(bad_resp.json()["features"]), 0)

class RouteAPITestCase(TestCase):
    """test route data API calls"""
    def test_mapbox_api(self):
        """test route data returning from mapbox API"""
        good_geostring = "-106.582998,35.191097;-106.540495,35.12415"
        bad_geostring = "35.191097,-106.582998;35.12415,-106.540495"
        success_resp = requests.get(f'{MB_DIRECTIONS_BASE_URL}cycling/{good_geostring}?alternatives=true&geometries=geojson&steps=true&access_token={MB_API_KEY}')
        fail_resp = requests.get(f'{MB_DIRECTIONS_BASE_URL}cycling/{bad_geostring}?alternatives=true&geometries=geojson&steps=true&access_token={MB_API_KEY}')

        self.assertEqual(success_resp.status_code, 200)
        self.assertIn("routes", success_resp.json())
        self.assertEqual(fail_resp.status_code, 422)
        self.assertIn("message", fail_resp.json())
        self.assertEqual(fail_resp.json()['code'], "InvalidInput")


###################################
##### Flask API calls from JS #####
###################################
class FlaskRouteAPITestCase (TestCase):
    """test Flask Route API cases"""
    def test_flask_routes_preview(self):
        """test that previewing routes are being handled correctly at '/api/routes/preview'"""
        good_route_qString = "?0-lat=37.746998&0-lng=-122.418653&999-lat=37.801237&999-lng=-122.40072"
        bad_route_qString = "?0-lng=37.746998&0-lat=-122.418653&999-lng=37.801237&999-lat=-122.40072"

        good_resp = requests.get(f'http://127.0.0.1:5000/api/routes/preview{good_route_qString}')
        bad_resp = requests.get(f'http://127.0.0.1:5000/api/routes/preview{bad_route_qString}')
        bad_url_resp = requests.get(f'http://127.0.0.1:5000/api/routes/preveiw{good_route_qString}')
        
        self.assertEqual(good_resp.status_code, 200)
        self.assertNotIn("Errors", good_resp.json())
        self.assertIn("routes", good_resp.json())
        self.assertEqual(bad_resp.status_code, 200)
        self.assertIn("Errors", bad_resp.json())
        self.assertEqual(bad_url_resp.status_code, 404)
