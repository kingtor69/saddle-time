// TODO: make browser location work

// mapLat and mapLng are generated in mapbox.js, which has already run when this does.
const unitsSelector = document.querySelector('#units-selector');
let units = unitsSelector.value;
const unitsOptionMetric = document.querySelector('option.metric-option')
const unitsOptionImperial = document.querySelector('option.imperial-option')
const weatherHeader = document.querySelector('#weather-header')
const weatherConditionsHeader = document.querySelector('#weather-conditions-row')
const weatherConditions = document.querySelector('#weather-conditions')
const weatherIcon = document.querySelector('#weather-icon')
const weatherDetails = document.querySelector('#weather-details')

// unitsSelector.addEventListener('change', function(evt) {
//     units = evt.target.value;
//     weather = updateWeather(units, geocode);
// });

async function updateWeather(units, geocode) {
    $('#flashes').hide()
let geocodeLat;
    let geocodeLng;
    if (geocodeLat > 90 || geocodeLat < -90) {
        throw new Error('Lattitude must be a number between -90 and 90.')
    }
    if (geocodeLng > 180 || geocodeLng < -180) {
        throw new Error('Longitute must be a number between -180 and 180.')
    }
    if (geocode) {
        geocodeLat = geocode[1];
        geocodeLng = geocode[0];
    } else {
        throw new Error('No geocode data makes it hard to find the weather.');
    }
    const weatherUrl = `/api/weather?location=${location}&units=${units}&lat=${geocodeLat}&lng=${geocodeLng}`;
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


// if (mapboxLocationSelectors.length === 1) {
//     weatherLocation = mapboxLocationSelectors;
//     weatherLocation.change((evt) => {
//         console.log(weatherLocation.select2('data'));
//     })
// } else {
    
// }

// this isn't working and currently deactivate
// TODO: fix and activate it
// browserLocationButton.addEventListener('click', function() {
//     const default_location = "949 Montoya St NW, Albuquerque, NM 87104"
//     // let nudge = document.getElementById("nudge");
  
//     // let showNudgeBanner = function() {
//     //   nudge.style.display = "block";
//     // };
  
//     // let hideNudgeBanner = function() {
//     //   nudge.style.display = "none";
//     // };
  
//     // let nudgeTimeoutId = setTimeout(showNudgeBanner, 5000);
  
//     let geoSuccess = function(position) {
//         lat = position.coords.latitude;
//         lng = position.coords.longitude;
//         geocode = [lat, lng];
//         updateWeather(null, units, (lat, lng))
//         // hideNudgeBanner();
//         // We have the location, don't display banner
//         // clearTimeout(nudgeTimeoutId); 
        
        
//         // Do magic with location
//         // document.getElementById('startLat').innerHTML = position.coords.latitude;
//         // document.getElementById('startLon').innerHTML = position.coords.longitude;
//     };

//     let geoError = function(error) {
//         updateWeather(default_location, units, null)
//     };
  
//     navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
// });

// TODO: add unitsSelector eventListener

function updateWeatherDOM(weather) {
    weatherConditionsHeader.innerHTML = ""
    // update city:
    // >>>>>>>>>> TODO: when this is accessed via the temperature change route, we get a big, fat nothing in weather.city
    // weatherCityInput.value = weather.city;
    // update units:
    if (weather.units === "imperial") {
        unitsOptionMetric.selected = '';
        unitsOptionImperial.selected = 'selected';
    } else if (weather.units === "metric") {
        unitsOptionMetric.selected = 'selected';
        unitsOptionImperial.selected = '';
    } else {
        throw new Error('invalid weather units');
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

async function geocodeFromLocation(location) {
    resp = await axios.get(`/api/location?location=${location}`);
    console.log(resp)
}

///////////////////////////
// location autocomplete //
///////////////////////////
// using Select2
// weather location only:

let weatherSelect2Data = selectTwo(weatherLocationSelector)

weatherLocationSelector.change((e) => {
    console.log(weatherSelect2Data);
    // weatherLocation = weatherLocationSelector.select2('data')[0].text;
    // localStorage.setItem('weatherLocation', weatherLocation);
    // const geocode = geocodeFromLocation(weatherLocation);
    // const weather = updateWeather(units, geocode);
    // localStorage.setItem('weather', weather);

});




// need to add class="mapbox-location-selector form-control" because apparently it goes away when select2 is turned on
// maybe because it's inside a Bootstrap "modal:"
// https://select2.org/troubleshooting/common-problems

