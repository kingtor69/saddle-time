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
    choiceDropdown.hidden = true;
    const inputSpanner = document.querySelector('.input-spanner');
    locInput.after(choiceDropdown);
    locInput.addEventListener('keypress', function(e) {
        e.preventDefault();
        
        const locData = locInput.value;

        let key = e.which || e.keyCode || 0;
        if (key === 13) {
            locData = locInput.placeholder;
            const latLong = getGeocode(locData);
        }
        
        choiceDropdown.hidden=false;
        
        if (locData.length >= 3) {
            autoCompleteChoices = locationWithAutocomplete(locData);
            console.log(autoCompleteChoices)
            locInput.placeholder = autoCompleteChoices[0];
            for (let choice in autoCompleteChoices) {
                const choiceLi = document.createElement('li');
                const selectButton = document.createElement('button');
                selectButton.classList.add('dropdown-selection');
                selectButton.innerHTML = `${choice[0]}<br><small>${choice[1]}</small>`
                choiceLi.appendChild(selectButton);
                choiceDropdown.appendChild(choiceLi);
            }
        }
    });
});

async function locationWithAutocomplete(location) {
    resp = await axios.get(`${mapboxGeocodeApiBaseUrl}${location}.json?autocomplete=true&access_token=${mapboxApiPublicToken}`);
    if (resp.message === "Not Found") {
        return [["no matches found", "please delete some characters and try again"]]
        };

    const choices = [];
    for (choice in resp.features) {
        choices.append([choice.text, choice.place_name])
    };
    return choices;
};

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

