const mapLat = document.querySelector('#map-lat').innerText;
const mapLng = document.querySelector('#map-lng').innerText;
const mapZoom = document.querySelector('#map-zoom').innerText;
const mapboxGeocodeApiBaseUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
let firstTime = true;

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
    // e.preventDefault();
    if (e.key === 'Enter' || e.key === 'Return') {
        // flashDiv.innerHTML = ""
        getLocationGeocode(locationSearch)
        // updateWeather(mapboxLocationInput.value, units);
    } else {
        if (!firstTime) {
            locationSearch = mapboxLocationInput.value;
        };
        firstTime = false;
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
    for (let feature of features) {
        choices.push([feature.text, feature.place_name])
    };
    displayChoices(choices, activeInput);
};

function displayChoices(choices, activeInput) {
    const autocompleteContainer = document.querySelector('div.autocomplete-container');
    autocompleteContainer.innerHTML = '';
    autocompleteContainer.classList = "autocomplete-container";
    const autocompleteMenu = document.createElement('ul');
    autocompleteMenu.classList.add("autocomplete-menu");
    autocompleteMenu.id = `${activeInput.id}-choices`
    autocompleteContainer.appendChild(autocompleteMenu);
    for (let i=0; i < 5; i++) {
        const choiceLi = document.createElement('li');
        choiceLi.classList.add('autocomplete-choice');
        liButton = document.createElement('button');
        liButton.classList.add('autocomplete-choice');
        liButton.innerHTML = `<b>${choices[i][0]}</b><br><small>${choices[i][1]}</small><hr>`;
        choiceLi.appendChild(liButton);
        autocompleteMenu.appendChild(choiceLi);
    };
    // for (let choice of choices) {
    //     const choiceLi = document.createElement('li');
    //     choiceLi.classList.add('autocomplete-choice');
    //     choiceLi.innerHTML = `<b>${choice[0]}</b><br><small>${choice[1]}</small><hr>`
    //     autocompleteMenu.appendChild(choiceLi);
    // };
    const inputParent = activeInput.parentElement;
    const nxtSib = activeInput.nextSibling;
    inputParent.insertBefore(autocompleteContainer, nxtSib);
    const selection = chooseFromList(autocompleteMenu) || choices[0][0];
    activeInput.value = selection;
};

// now pick the winner
// TODO: THIS DOESN'T WORK
function chooseFromList(menu) {
    let selectedLi = menu.querySelector('li#hero') || null;
    // TODO this keydown listener isn't working at all
    menu.addEventListener('keydown', function(e) {
        if (e.keyCode === 40) {
            // down arrow
            console.log('down')
            if (selectedLi) {
                selectedLi.id = false;
                selectedLi = selectedLi.nextSibling();
            };
            selectedLi.id = 'hero';
        } else if (e.keyCode === 38) {
            //  up arrow
            console.log('up')
            if (selectedLi) {
                selectedLi = selectedLi.previousSibling() || null;
            };
            if (selectedLi) {
                selectedLi.id = "hero";
            };
        } else if (e.keyCode === 13) {
            // enter
            selectionHTML = selectedLi.firstChild.innerHTML;
            return chooseChoice(selectionHTML);
        };
    });
    menu.querySelectorAll('button.autocomplete-choice').forEach(button => {
        button.addEventListener('click', function(e) {
            const selectionHTML = button.innerHTML;
            return chooseChoice(selectionHTML);
        });
    });
};

function chooseChoice(selectionHTML) {
    let selection = "";
    let on = false;
    for (let char in selectionHTML) {
        if (on) {
            selection += char;
        } else if (char === '>') {
            on = true;
        } else if (char === '<') {
            return selection;
        };
    };
};