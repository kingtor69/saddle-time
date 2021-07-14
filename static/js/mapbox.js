const mapLat = document.querySelector('#map-lat').innerText;
const mapLng = document.querySelector('#map-lng').innerText;
const mapZoom = document.querySelector('#map-zoom').innerText;
const mapboxGeocodeApiBaseUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

mapboxgl.accessToken = 'pk.eyJ1Ijoia2luZ3RvciIsImEiOiJja3A2ZmdtNmwyaHBlMnZtd2xxMmJ3Z3ljIn0.YpzXxkn-7AwHzZpWapeFjQ';
var map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [mapLng, mapLat], // starting position [lng, lat]
    zoom: mapZoom // starting zoom
});
map.addControl(new mapboxgl.NavigationControl());
map.on('load', function() {
    map.loadImage('static/images/mapbox-icons/mapbox-marker-icon-20px-red.png', function (error, image) {
        if (error) throw error;
        map.addImage('redPointer', image);
        map.addSource('point', {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': [
                    {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [mapLng, mapLat]
                        }
                    }
                ]
            }
        });
            
        // Add a layer to use the image to represent the data.
        map.addLayer({
            'id': 'points',
            'type': 'symbol',
            'source': 'point', // reference the data source
            'layout': {
                'icon-image': 'redPointer', // reference the image
                'icon-size': 1
            }
        });
    })
})

function geocodeFromLocation(location) {
    
}

///////////////////////////
// location autocomplete //
///////////////////////////
// first doing this with only one on the
// then it will have to be adapted to handle more than one on a page
const mapboxLocationInput = document.querySelector('input.mapbox-location-input')
let locationSearch = ""
// let geocodeLat
// let geocodeLng

mapboxLocationInput.addEventListener('click', function() {
    mapboxLocationInput.focus();
    mapboxLocationInput.select();
    mapboxLocationInput.classList.remove('location-is-set');
});

mapboxLocationInput.addEventListener('keypress', function(e) {
    e.preventDefault();
    if (e.key === 'Enter' || e.key === 'Return') {
        // flashDiv.innerHTML = ""
        getLocationGeocode(locationSearch)
        // updateWeather(mapboxLocationInput.value, units);
    } else {
        locationSearch += e.key;
        if (locationSearch.length >= 3) {
            locationAutocomplete(locationSearch, mapboxLocationInput);
        };
    };
});

async function getLocationGeocode(location) {
    flashDiv.hidden = true;
    mapboxLocationInput.classList.add('location-is-set');
    geocodeJSON = await axios.get(`${mapboxGeocodeApiBaseUrl}${locationSearch}.json?access_token=${mapboxgl.accessToken}`);
    console.log(`geocodeJSON is`);
    console.log(geocodeJSON);
};

async function locationAutocomplete(locationSearch, activeInput) {
    resp = await axios.get(`${mapboxGeocodeApiBaseUrl}${locationSearch}.json?autocomplete=true&access_token=${mapboxgl.accessToken}`);
    features = resp.data.features;
    choices = [];
    for (let feature in features) {
        choices.push([feature.text, feature.place_name])
    };
    displayChoices(choices, activeInput);
};

function displayChoices(choices, activeInput) {
    const choicesDisplay = document.createElement('div');
    choicesDisplay.classList = "dropdown-menu";
    console.log(choices)
    for (let choice of choices) {
        const choiceDiv = document.createElement('div');
        choiceDiv.classList = "dropdown-item";
        choiceDiv.innerHTML = `<b>${choice[0]}</b><br>${choice[1]}`
        choicesDisplay.appendChild(choiceDiv);
    };
    const inputParent = activeInput.parentElement;
    const nxtSib = activeInput.nextSibling;
    inputParent.insertBefore(choicesDisplay, nxtSib);
    console.log(inputParent);
};
