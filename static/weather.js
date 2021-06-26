/////////////////////////////////////
// weather location button/input on home page
// this was one way it kinda worked:
////////////////////////////////////
// const weatherCityChoice = document.querySelector('#weather-city')
// const weatherCityForm = document.querySelector('#change-city')
// const weatherCityInput = document.querySelector('#weather-city-input')
// const messageOrLocation = document.querySelectorAll('.message-or-use-location')

// weatherCityChoice.addEventListener('click', function(e) {
//   e.preventDefault()
//   weatherCityChoice.classList.add('d-none')
//   weatherCityInput.classList.remove('d-none')
//   weatherCityInput.focus();
//   weatherCityInput.select();
//   for (let field of messageOrLocation) {
//     field.classList.toggle('d-none')
//   }
// })

// this might be better
/////////////////////////////////////
const weatherCityInput = document.querySelector('#weather-city-input');
const browserLocation = document.querySelector('#browser-location-select');
const unitsSelector = document.querySelector('#units-selector')

weatherCityInput.addEventListener('click', function() {
    weatherCityInput.focus();
    weatherCityInput.select();
    weatherCityInput.classList.remove('city-is-set')
})
weatherCityInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' || e.key === 'Return') {
      weatherCityInput.classList.add('city-is-set');
      reloadHomePageWithNewLocation(weatherCityInput.value, unitsSelector.value);
    }
})



async function reloadHomePageWithNewLocation(location, units) {
    console.log ('reload home page.... now?')
    await axios({
        method: 'post',
        url: '/',
        data: {
            location: location,
            units: units
        }
    })
}

// here's a weird thing.... when I added this async function, weatherCityInput.select(); stopped working
// async getWeather(location) {
//     weatherResponse = await axios.get()
// }
// also, rewriting the geocoding *and* getWeather API calls in JS seems like a waste of time, so I'm looking at how to do this in Python/Flask

// const useBrowserLocation = document.querySelector('#use-browser-location')

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
        reloadHomePageWithNewLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
        })
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