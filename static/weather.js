// weather location button/input and units-selector on home page
// TODO: make unitsSelector work
const weatherCityInput = document.querySelector('#weather-city-input');
const browserLocation = document.querySelector('#browser-location-select');
const unitsSelector = document.querySelector('#units-selector');
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
        updateWeather(weatherCityInput.value, unitsSelector.value);
    };
});

async function updateWeather(location, units, geocode) {
    const weatherUrl = `${baseApiUrl}weather?location=${location}&units=${units}&geocode=${geocode}`;
    console.log(weatherUrl);
    resp = await axios.get(weatherUrl);
    if (resp.data.Errors) {
        errorObj = resp.data.Errors;
        errorArr = [];
        for (let error in errorObj) {
            if (errorObj[error] !== "No valid geocode entered.") {
                errorArr.push([error, errorObj[error]]);
            };
        };
        displayErrors(errorArr);
    } else {
        // 
        // is it me?
        updateWeatherDOM(resp.data);
    };
};

function updateWeatherDOM(weather)) {
    console.log("TODO: why the eff can't I pass an object into a function anymore?")
    console.log(`see? updateWeatherDOM(${weather})`)
};

//////////////////////////// this isn't working, but it's here:
browserLocation.addEventListener('click', function() {
    const default_location = "Albuquerque, NM 87102 USA"
    let theyAreHere;
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
      theyAreHere = default_location
    };
  
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
  });