// TODO: make unitsSelector work
// TODO: make browser location work
// weather location button/input and units-selector on home page
const weatherCityInput = document.querySelector('#weather-city-input');
const browserLocationButton = document.querySelector('#browser-location-select');
const unitsSelector = document.querySelector('#units-selector');
let units = unitsSelector.value;
const unitsOptionMetric = document.querySelector('option.metric-option')
const unitsOptionImperial = document.querySelector('option.imperial-option')
const weatherHeader = document.querySelector('#weather-header')
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
        displayErrors(errorObj);
    } else {
        updateWeatherDOM(resp.data);
    };
};

//TODO: this isn't working, but it's here:
browserLocationButton.addEventListener('click', function() {
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
    // update city:
    weatherCityInput.value = weather.city;
    // update units:
    if (weather.units === "imperial") {
        unitsOptionMetric.selected = '';
        unitsOptionImperial.selected = 'selected';
    } else {
        unitsOptionMetric.selected = 'selected';
        unitsOptionImperial.selected = '';
    }
    // update conditions headline
    weatherConditions.innerText = weather.conditions;
    weatherIcon.innerHTML = `<img src="${weather.weather_icon_url}">`
    weatherConditionsHeader.appendChild(weatherConditions)
    weatherConditionsHeader.appendChild(weatherIcon)
    
    // gather DOM and data for details
    weatherDetailKeysTds = document.querySelectorAll('td.weather-detail-key')
    weatherDetailValueTds = document.querySelectorAll('td.weather-detail-value')
    const weatherDetailObj = weather.current_weather_details
    
    // now put the right values in the existing keys
    for (let i=0; i<weatherDetailKeysTds.length; i++) {
        weatherDetailValueTds[i].innerText = weatherDetailObj[weatherDetailKeysTds[i].innerText]
    }
    return `
        ${weatherConditionsHeader.innerHTML}
        ${weatherDetails.innerHTML}
    `
};

