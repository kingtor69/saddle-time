import os
from unittest import TestCase
from helpers import *
import requests

from app import app

class GeocodeParsingTestCase(TestCase):
    """test the functioning of parse_geocode"""
    def test_parse_geocode(self):
        orderly_args = {'0-lng': '-102.9248', '0-lat': '31.2593', '3-lng': '-103.0001', '3-lat': '31.1948', '999-lng': '-103.1123', '999-lat': '30.8374'}

        semi_orderly_args = {'0-lng': '-102.9248', '0-lat': '31.2593', '999-lng': '-103.1123', '999-lat': '30.8374', '3-lng': '-103.0001', '3-lat': '31.1948'}

        disorderly_args = {'0-lat': '31.2593', '0-lng': '-102.9248', '999-lng': '-103.1123', '3-lng': '-103.0001', '999-lat': '30.8374', '3-lat': '31.1948'}

        expected_geocode = '-102.9248,31.2593;-103.0001,31.1948;-103.1123,30.8374'

        not_enough_data_args = {'0-lat': '31.2593', '999-lng': '-103.1123', '3-lat': '31.1948', '3-lng': '-103.0001'}

        # this error handling is in JS, so I don't think I need to (or can) test it here
        # bad_data = {'0-lat': '-103.1123', '0-lng': '31.2593', '999-lat': '-103.0001', '999-lng': '31.1948'}

        irl_args = {'0-lat': '37.746998', '0-lng': '-122.418653', '999-lat': '37.801237', '999-lng': '-122.40072'}

        sortable_irl_args = {'0': {'lat': '37.746998', 'lng': '-122.418653'}, '999': {'lat': '37.801237', 'lng': '-122.40072'}}

        irl_url = "http://127.0.0.1:5000/routes/new?0-lat=37.746998&0-lng=-122.418653&999-lat=37.801237&999-lng=-122.40072"

        expected_irl_code = '-122.418653,37.746998;-122.40072,37.801237'

        self.assertEqual(
            parse_geocode(orderly_args), expected_geocode
        )
        self.assertEqual(
            parse_geocode(semi_orderly_args), expected_geocode
        )
        self.assertEqual(
            parse_geocode(disorderly_args), expected_geocode
        )

        self.assertRaises(
            KeyError, 
            parse_geocode,
            not_enough_data_args 
        )

        # this error handling is in JS, so I don't think I need to (or can) test it here
        # self.assertRaises(
        #     Error,
        #     parse_geocode,
        #     bad_data
        # )


# orderly_route_qString = "0-lng=-102.9248&0-lat=31.2593&3-lng=-103.0001&3-lat=31.1948&999-lng=-103.1123&999-lat=30.8374"

# semi_orderly_route_qString = "0-lng=-102.9248&0-lat=31.2593&999-lng=-103.1123&999-lat=30.8374&3-lng=-103.0001&3-lat=31.1948"