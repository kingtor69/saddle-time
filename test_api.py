import os
from unittest import TestCase
from helpers import *
import requests

from app import app

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

class WeatherAPITestCase (TestCase):
    """test that weather API calls are returning valid data"""

class RouteAPITestCase (TestCase):
    """test Flask API cases"""
    def test_flask_routes_route(self):
        """test that data coming from JS to Flask routes '/api/routes' are working properly"""
        good_route_qString = "?0-lat=37.746998&0-lng=-122.418653&999-lat=37.801237&999-lng=-122.40072"
        bad_route_qString = "?0-lng=37.746998&0-lat=-122.418653&999-lng=37.801237&999-lat=-122.40072"

        good_resp = requests.get(f'/api/routes/new{good_route_qString}')
        bad_resp = requests.get(f'/api/routes/preview{bad_route_qString}')
        
        self.assertEqual(good_resp.status_code, 200)
        # self.assertEqual(bad_resp.status_code, 404)



    def test_mapbox_route_API(self):
        """test mapbox API calls """

