const mapboxGeocodeApiBaseUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
const mapboxApiPublicToken = "pk.eyJ1Ijoia2luZ3RvciIsImEiOiJja3A2ZmdtNmwyaHBlMnZtd2xxMmJ3Z3ljIn0.YpzXxkn-7AwHzZpWapeFjQ"

const lat = document.querySelector('#map-lat').innerText;
const lng = document.querySelector('#map-lng').innerText;
const zoom = document.querySelector('#map-zoom').innerText;
const locationInputs = document.querySelectorAll('input.mapbox-loction-input')

locationInputs.forEach((locInput) => {
    locInput.addEventListener('click', function() {
        locInput.focus();
        locInput.select();
        locInput.classList.remove('location-is-set');
    });
    
    const choiceDropdown = document.createElement('ul');
    choiceDropdown.classList.add('location-choices-list');
    choiceDropdown.id = "choice-dropdown";
    choiceDropdown.hidden = true;
    const inputSpanner = document.querySelector('.input-spanner');
    locInput.after(choiceDropdown);
    let locData = "";
    locInput.addEventListener('keypress', function(e) {
        const key = e.key;
        let latLong;
        if (key === "Enter") {
            locData = locInput.placeholder;
            latLong = getGeocode(locData);
        } else {
            locData += key;
        };
        
        if (locData.length >= 3) {
            locateWithAutocomplete(locData, locInput);
        }
    });
});

async function locateWithAutocomplete(location, input) {
    // gets autocomplete data from mapbox for location
    // input is passed through to processing function
    const geocodeURL = `${mapboxGeocodeApiBaseUrl}${location}.json?autocomplete=true&access_token=${mapboxApiPublicToken}`
    const choices = [];
    resp = await axios.get(geocodeURL);
    if (resp.data.message === "Not Found") {
        choices.push(["no matches found", "please delete some characters and try again"])
    } else if (resp.data.features) {
        for (choice in resp.data.features) {
            choices.push([choice.text, choice.place_name])
        };
    };

    processLocationData(choices, input);
};

function processLocationData (choices, locInput) {
    const choiceDropdown = document.querySelector('#choice-dropdown');
    choiceDropdown.hidden=false;
    locInput.placeholder = choices[0];
    for (let choice in choices) {
        const choiceLi = document.createElement('li');
        const selectButton = document.createElement('button');
        selectButton.classList.add('dropdown-selection');
        selectButton.innerHTML = `${choice[0]}<br><small>${choice[1]}</small>`
        choiceLi.appendChild(selectButton);
        choiceDropdown.appendChild(choiceLi);
    }
}


async function getGeocode(location) {
    console.log("haven't written this yet");
}

mapboxgl.accessToken = 'pk.eyJ1Ijoia2luZ3RvciIsImEiOiJja3A2ZmdtNmwyaHBlMnZtd2xxMmJ3Z3ljIn0.YpzXxkn-7AwHzZpWapeFjQ';
let map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [ lng, lat ], // starting position
  zoom: zoom // starting zoom
});
map.addControl(new mapboxgl.NavigationControl());

// Add geocoding control to the map:
// TODO: why isn't that working?
// map.addControl(
//     new Mapboxgeocoder({
//         accessToken: mapboxgl.accessToken,
//         mapboxgl: mapboxgl
//     })
// );

