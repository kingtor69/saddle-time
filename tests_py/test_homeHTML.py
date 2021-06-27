import os
from unittest import TestCase
from secrets import ORS_API_KEY, MQ_API_KEY, OW_API_KEY
import requests

from app import app
from routes import test_routes

class WeatherHtmlTestCase (TestCase):
    """test that weather data is being presented on the home page"""
    weather_test_dic = {
        "city": "Albuquerque",
        "conditions": "Scattered Clouds",
        "weather_icon_url": "http://openweathermap.org/img/wn/03d@2x.png"
        "current_weather_details": {
            "Temperature": "25.0℃",
            "Feels Like": "24.6℃",
            "High": "28.0℃",
            "Low": "16.9℃",
            "Relative Humidity": "39%",
            "Wind Speed": "1.8 km/h",
            "Wind Direction": "33° Northeasterly"
        }
    }
    weather_test_html_details = """
        <tbody id="weather-details">
          
          <tr>
            <td>Temperature</td>
            <td>25.0℃</td>
          </tr>
          
          <tr>
            <td>Feels Like</td>
            <td>24.6℃</td>
          </tr>
          
          <tr>
            <td>High</td>
            <td>28.0℃</td>
          </tr>
          
          <tr>
            <td>Low</td>
            <td>16.9℃</td>
          </tr>
          
          <tr>
            <td>Relative Humidity</td>
            <td>39%</td>
          </tr>
          
          <tr>
            <td>Wind Speed</td>
            <td>1.79 km/h</td>
          </tr>
          
          <tr>
            <td>Wind Direction</td>
            <td>33° Northeasterly</td>
          </tr>
          
        </tbody>
    """

    weather_test_html_conditions_header = """
        <tr id="weather-conditions-row">
          <th class="h3" id="weather-conditions">Scattered Clouds </th>
          <th id="weather-icon"><img src="http://openweathermap.org/img/wn/03d@2x.png"></th>
        </tr>
    """

    def test_weather_display(self):
        """test weather is displaying correctly on home page using default weather settings (landing page, no JavaScript)"""
        with app.test_client() as client:
            res = client.get(f'/home_test?weather={weather_test_dic}')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button type="submit" class="btn btn-default">Submit</button>', html)
