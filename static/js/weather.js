console.log('weather.js');
// mapLat and mapLng are generated in mapbox.js, which has already run when this does.
const unitsSelector = document.querySelector('#units-selector');
const unitsOptionMetric = document.querySelector('option.metric-option');
const unitsOptionImperial = document.querySelector('option.imperial-option');
const weatherHeader = document.querySelector('#weather-header');
const weatherConditionsHeader = document.querySelector('#weather-conditions-row');
const weatherConditions = document.querySelector('#weather-conditions');
const weatherIcon = document.querySelector('#weather-icon');
const weatherDetails = document.querySelector('#weather-details');

selectTwo(weatherLocationSelector);

const queryString = parseCurrentQueryString();
let weatherLocation = weatherLocationSelector.select2('data')[0].text; defaultLocation; 
let units = queryString.units; unitsSelector.value;

if (queryString.location) {
    weatherLocation = queryString.location;
} else if (queryString.lat && queryString.lng) {
    weatherLocation = axios.get(`/api/location?lat=${queryString.lat}&lng=${queryString.lng}`);
    weatherLocation.then(resp => {
        return resp.data.location;
    });
};

unitsSelector.addEventListener('change', function(evt) {
    units = evt.target.value;
    localStorage.setItem('units', units);
    weather = updateWeather(units, mapLat, mapLng);
    updateUrl({"location": weatherLocation, "latitude": mapLat, "longitude": mapLng, "units": units});
});

async function updateWeather(units, lat, lng) {
    $('#flashes').hide()
    if (lat > 90 || lat < -90) {
        throw new Error('Lattitude must be a number between -90 and 90.')
    }
    if (lng > 180 || lng < -180) {
        throw new Error('Longitute must be a number between -180 and 180.')
    }
    const weatherUrl = `/api/weather?units=${units}&lat=${lat}&lng=${lng}`;
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
    } else if (!resp.data) {
        displayErrors({'error': `no data returned from ${weatherUrl}`});
    } else {
        updateWeatherDOM(resp.data, lat, lng);
    };
};

function updateWeatherDOM(weather, lat, lng) {
    weatherConditionsHeader.innerHTML = ""
    if (weather.units === "imperial") {
        unitsOptionMetric.selected = '';
        unitsOptionImperial.selected = 'selected';
    } else if (weather.units === "metric") {
        unitsOptionMetric.selected = 'selected';
        unitsOptionImperial.selected = '';
    } else {
        throw new Error('invalid weather units');
    }

    weatherConditions.innerText = weather.conditions;
    weatherIcon.innerHTML = `<img src="${weather.weather_icon_url}">`
    weatherConditionsHeader.appendChild(weatherConditions)
    weatherConditionsHeader.appendChild(weatherIcon)

    // gather DOM and data for details
    weatherDetailKeysTds = document.querySelectorAll('td.weather-detail-key')
    weatherDetailValueTds = document.querySelectorAll('td.weather-detail-value')
    const weatherDetailObj = weather.current_weather_details
    
    for (let i=0; i<weatherDetailKeysTds.length; i++) {
        weatherDetailValueTds[i].innerText = weatherDetailObj[weatherDetailKeysTds[i].innerText]
    };

    const inputMapLat = document.querySelector('#map-center-lat');
    const inputMapLng = document.querySelector('#map-center-lng');
    inputMapLat.value = lat;
    inputMapLng.value = lng;

    return `
        ${weatherConditionsHeader.innerHTML}
        ${weatherDetails.innerHTML}
    `
};

async function geocodeFromLocation(location) {
    resp = await axios.get(`/api/geocode?location=${location}`);
    lat = resp.data[0][0];
    lng = resp.data[0][1];
    return [lat, lng]
}

async function geocodeFromMapboxLocation(locationId) {
    resp = await axios.get(`/api/geocode?id=${locationId}`)
}

///////////////////////////
// location autocomplete //
////// using Select2 //////
///////////////////////////
weatherLocationSelector.change((e) => {
    const [units, mapLat, mapLng] = processAutocomplete(e, weatherLocationSelector, 'weather');
    updateWeather(units, mapLat, mapLng);
    centerMap(mapLat, mapLng);
    // console.log('remove bluePointer?');
    // if (map.hasImage(`bluePointer`)) { map.removeImage(`bluePointer`) };
    placeMarker('blue', 'urhere', mapLat, mapLng);
});