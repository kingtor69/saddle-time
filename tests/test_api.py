import os
from unittest import TestCase
from flask import jsonify
from helpers import *
import requests

from app import app


##############################
##### external API calls #####
##############################
class GeocodeAPITestCase(TestCase):
    """Test retrieving geocode information from Mapquest API"""
    def test_geocoding_method(self):
        good_loc = "9201 Pan American FWY NE, Albuquerque, NM 87113"
        good_code = (35.190564, -106.580526)
        unfound_loc = ";"
        mult_choice_loc = "Albuquerque"
        mult_choice0_code = (35.084248, -106.649241)
        mult_choice1_code = (-22.383301, -42.916599)

        self.assertEqual(geocode_from_location_mq(good_loc)[0], good_code)
        self.assertFalse(geocode_from_location_mq(unfound_loc))
        self.assertEqual(len(geocode_from_location_mq(mult_choice_loc)), 2)
        self.assertEqual((geocode_from_location_mq(mult_choice_loc)), [mult_choice0_code, mult_choice1_code])

    def test_geocoding_API_call(self):
        good_loc = "9201 Pan American FWY NE, Albuquerque, NM 87113"
        good_code = (35.190564, -106.580526)
        unfound_loc = ";"
        mult_choice_loc = "Albuquerque"
        mult_choice0_code = (35.084248, -106.649241)
        mult_choice1_code = (-22.383301, -42.916599)

        good_resp=requests.get(f'{MQ_API_BASE_URL}/address?key={MQ_API_KEY}&location={good_loc}')
        good_results = good_resp.json()
        good_lat_lng = good_results["results"][0]["locations"][0]["latLng"]
        unfound_resp=requests.get(f'{MQ_API_BASE_URL}/address?key={MQ_API_KEY}&location={unfound_loc}')

        mult_choice_resp=requests.get(f'{MQ_API_BASE_URL}/address?key={MQ_API_KEY}&location={mult_choice_loc}')
        mult_choice_results=mult_choice_resp.json()
        mult_choice0_lat_lng=mult_choice_results["results"][0]["locations"][0]["latLng"]
        mult_choice1_lat_lng=mult_choice_results["results"][0]["locations"][1]["latLng"]
        mult_choice_results = mult_choice_resp.json()

        self.assertEqual(
            (good_lat_lng["lat"], good_lat_lng["lng"]), good_code
        )
        self.assertEqual(
            len(mult_choice_results["results"][0]["locations"]), 2
        )
        self.assertEqual(
            (mult_choice0_lat_lng["lat"], mult_choice0_lat_lng["lng"]), 
            mult_choice0_code
        )
        self.assertEqual(
            (mult_choice1_lat_lng["lat"], mult_choice1_lat_lng["lng"]), 
            mult_choice1_code
        )            

class RouteAPITestCase(TestCase):
    """test route data API calls"""
    def test_mapbox_api(self):
        """test route data returning from mapbox API"""
        good_geostring = "-106.582998,35.191097;-106.540495,35.12415"
        success_resp = requests.get(f'{MB_DIRECTIONS_BASE_URL}cycling/{good_geostring}?alternatives=true&geometries=geojson&steps=true&access_token={MB_API_KEY}')

        self.assertEqual(success_resp.status_code, 200)


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
        very_bad_url_resp = requests.get(f'http://127.0.0.1:5000/api/routes/preveiw{good_route_qString}')
        
        self.assertEqual(good_resp.status_code, 200)
        self.assertNotIn("Errors", good_resp.json())
        self.assertIn("routes", good_resp.json())
        self.assertEqual(bad_resp.status_code, 200)
        self.assertIn("Errors", bad_resp.json())
        self.assertEqual(bad_url_resp.status_code, 500)
        self.assertEqual(very_bad_url_resp.status_code, 404)


#########################################
## RESTful API calls from JS via Flask ##
#########################################
# class RESTfulRoutesTestCase (TestCase):
#     """test RESTful API calls for 'routes' table"""
#     def test_routes_create(self):
#         """testing POST to '/api/routes'"""
#         good_route_post = jsonify({
#             'route': {
#                 'user_id': 1
#             }
#         })