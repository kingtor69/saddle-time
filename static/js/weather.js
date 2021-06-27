// weather location button/input and units-selector on home page
// TODO: make unitsSelector work
const weatherCityInput = document.querySelector('#weather-city-input');
const browserLocation = document.querySelector('#browser-location-select');
const unitsSelector = document.querySelector('#units-selector');
let units = unitsSelector.value;
const unitsOptionMetric = document.querySelector('option.metric-option')
const unitsOptionImperial = document.querySelector('option.imperial-option')
const weatherConditionsHeader = document.querySelector('#weather-conditions-row')
const weatherConditions = document.querySelector('#weather-conditions')
const weatherIcon = document.querySelector('#weather-icon')
const weatherDetails = document.querySelector('#weather-details')


const baseApiUrl = "/api/";

weatherCityInput.addEventListener('click', function() {
    weatherCityInput.focus();
    weatherCityInput.select();
    weatherCityInput.classList.remove('city-is-set');
});

weatherCityInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' || e.key === 'Return') {
        errorDiv.innerHTML = ""
        weatherCityInput.classList.add('city-is-set');
        updateWeather(weatherCityInput.value, units);
    };
});

async function updateWeather(location, units, geocode) {
    const weatherUrl = `${baseApiUrl}weather?location=${location}&units=${units}&geocode=${geocode}`;
    resp = await axios.get(weatherUrl);
    if (resp.data.Errors) {
        rawErrorObj = resp.data.Errors;
        errorObj = {}
        for (let error in rawErrorObj) {
            if (rawErrorObj[error] !== "No valid geocode entered.") {
                errorObj[error] = rawErrorObj[error];
            };
        };
        console.log(errorObj)
        displayErrors(errorObj);
    } else {
        updateWeatherDOM(resp.data);
    };
};

//TODO: this isn't working, but it's here:
browserLocation.addEventListener('click', function() {
    const default_location = "Albuquerque, NM 87102 USA"
    // let nudge = document.getElementById("nudge");
  
    // let showNudgeBanner = function() {
    //   nudge.style.display = "block";
    // };
  
    // let hideNudgeBanner = function() {
    //   nudge.style.display = "none";
    // };
  
    // let nudgeTimeoutId = setTimeout(showNudgeBanner, 5000);
  
    let geoSuccess = function(position) {
        updateWeather(null, units, (
            position.coords.latitude,
            position.coords.longitude
            ))
        // hideNudgeBanner();
        // We have the location, don't display banner
        // clearTimeout(nudgeTimeoutId); 
 
        
        // Do magic with location
        // document.getElementById('startLat').innerHTML = position.coords.latitude;
        // document.getElementById('startLon').innerHTML = position.coords.longitude;
    };

    let geoError = function(error) {
        updateWeather(default_location, units, null)
    };
  
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
  });

// TODO: add unitsSelector eventListener

function updateWeatherDOM(weather) {
    weatherConditionsHeader.innerHTML = ""
    weatherDetails.innerHTML = ""
    weatherCityInput.value = weather.city;
    if (weather.units === "imperial") {
        unitsOptionImperial.selected = 'selected';
    } else {
        unitsOptionMetric.selected = 'selected';
    }
    weatherConditions.innerText = weather.conditions;
    weatherIcon.innerHTML = `<img src="{{ weather['weather_icon_url'] }}" />`
    // this does it in alphabetical order... wtf?
    let weatherDetailsObj = weather.current_weather_details;
    console.log(weatherDetailsObj);
    // for (let detail in weatherDetailsObj) {
    //     const weatherTr = document.createElement('tr');
    //     const categoryTd = document.createElement('td');
    //     const conditionTd = document.createElement('td');
    //     categoryTd.innerText = detail;
    //     conditionTd.innerText = weather.current_weather_details[detail];
    //     weatherTr.appendChild(categoryTd);
    //     weatherTr.appendChild(conditionTd);
    //     weatherDetails.appendChild(weatherTr);
    // }
    weatherDetailsKeys = keys(weatherDetailsObj);
    for (let i=0; i < weatherDetailKeys.length; i++) {
        console.log(`key ${i}: ${weatherDetailKeys[i]}`)        
    //     const weatherTr = document.createElement('tr');
    //     const categoryTd = document.createElement('td');
    //     const conditionTd = document.createElement('td');
    //     categoryTd.innerText = detail;
    //     conditionTd.innerText = weather.current_weather_details[detail];
    //     weatherTr.appendChild(categoryTd);
    //     weatherTr.appendChild(conditionTd);
    //     weatherDetails.appendChild(weatherTr);
    }
    // temp = weather.current_weather_details["Temperature"]
    // feelsLike = weather.current_weather_details["Feels Like"]
    // high = weather.current_weather_details["High"]
    // low = weather.current_weather_details["Low"]
    // humidity = weather.current_weather_details["Relative Humidity"]
    // windSpeed = weather.current_weather_details["Wind Speed"]
    // windDirection = weather.current_weather_details["Wind Direction"]

};

