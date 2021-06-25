console.log('u r here. r they?')

const weatherCityChoice = document.querySelector('#weather-city')
const weatherCityForm = document.querySelector('#change-city')
const weatherCityInput = document.querySelector('#weather-city-input')
const messageOrLocation = document.querySelectorAll('.message-or-use-location')

weatherCityChoice.addEventListener('click', function(e) {
  e.preventDefault()
  weatherCityChoice.classList.add('d-none')
  weatherCityInput.classList.remove('d-none')
  weatherCityInput.focus();
  weatherCityInput.select();
  for (let field of messageOrLocation) {
    field.classList.toggle('d-none')
  }
})


const useBrowserLocation = document.querySelector('#use-browser-location')

useBrowserLocation.onclick = function() {
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
    //   hideNudgeBanner();
      // We have the location, don't display banner
    //   clearTimeout(nudgeTimeoutId); 
  
      // Do magic with location
      theyAreHere = position;
      document.getElementById('startLat').innerHTML = theyAreHere.coords.latitude;
      document.getElementById('startLon').innerHTML = theyAreHere.coords.longitude;
    };

    let geoError = function(error) {
      theyAreHere = default_location
    };
  
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError);
  };