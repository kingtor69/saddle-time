// I can't figure out where to put this test so that it works.

const testWeatherObj = {
    "city": "Albuquerque",
    "conditions": "Scattered Clouds",
    "weather_icon_url": "http://openweathermap.org/img/wn/03d@2x.png",
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

// TODO: This needs adapting from Jinja to reality
const testWeatherInformationHeaderRowHTML = `
  <tr id="weather-header-selectors">
    <th class="pt-4 my-3">
      <div class="row justify-content-left">
          <span id="weather-header">
            Current weather in: &nbsp;
            <input type="text" class="weather-city     city-is-set" id="weather-city-input" value="{{     weather.city }}">
          </span>
          <small class="text-muted"     id="weather-city-directions"><i>click city to     change</i> or <button     id="browser-location-select" class="">click here     to use broswer location</button></small>
      </div>
    </th>
    <th class="form-floating">
      <!-- this form in Python/Flask -->
      <form action="/" method="POST" id="weather-units"     class="d-inline">
        <select id="units-selector" class="form-select py-0     my-0 px-4 bg-info" id="unitSelect"     aria-label="Floating label select example">
          {% if weather_units == 'imperial' %}
            <option class="metric-option" value="metric">℃/    kmph</option>
            <option class="imperial-option" selected     value="imperial">℉/mph</option>
          {% else %}
            <option class="metric-option" selected     value="metric">℃/kmph</option>
            <option class="imperial-option"     value="imperial">℉/mph</option>
          {% endif %}
        </select>
      </form>
    </th>
  </tr>
`
const testWeatherConditionsHeaderHTML = `
  <tr id="weather-conditions-row">
    <th class="h3" id="weather-conditions">Scattered   Clouds</th>
    <th id="weather-icon"><img src="http://openweathermap.  org/img/wn/03d@2x.png" /></th>
  </tr>
`

const testTemperatureTd = '<td class="weather-detail-value">25.0℃</td>'
const testFeelsLikeTd = '<td class="weather-detail-value">24.6℃</td>'
const testWindDirectionTd = '<td class="weather-detail-value">33° Northeasterly</td>'

const testWeatherDetailsHTML = `




          <tr>
            <td class="weather-detail-key">Temperature</td>
            <td class="weather-detail-value">25.0℃</td>
          </tr>
          <tr>
            <td class="weather-detail-key">Feels Like</td>
            <td class="weather-detail-value">24.6℃</td>
          </tr>
          <tr>
            <td class="weather-detail-key">High</td>
            <td class="weather-detail-value">28.0℃</td>
          </tr>
          <tr>
            <td class="weather-detail-key">Low</td>
            <td class="weather-detail-value">16.9℃</td>
          </tr>
          <tr>
            <td class="weather-detail-key">Relative Humidity</td>
            <td class="weather-detail-value">39%</td>
          </tr>
          <tr>
            <td class="weather-detail-key">Wind Speed</td>
            <td class="weather-detail-value">1.8 km/h</td>
          </tr>
          <tr>
            <td class="weather-detail-key">Wind Direction</td>
            <td class="weather-detail-value">33° Northeasterly</td>
          </tr>
`


describe('weather display to home page', function() {
    it('should show the weather on the home page given a specific weather input', function() {
        expect(updateWeatherDOM(testWeatherObj).indexOf(testTemperatureTd) !== -1).toBe(true)
        expect(updateWeatherDOM(testWeatherObj).indexOf(testFeelsLikeTd) !== -1).toBe(true)
        expect(updateWeatherDOM(testWeatherObj).indexOf(testWindDirectionTd) !== -1).toBe(true)
    })
})