const mapLat = document.querySelector('#map-lat').innerText;
const mapLng = document.querySelector('#map-lng').innerText;
const mapZoom = document.querySelector('#map-zoom').innerText;
const locSelectors = Array.from(document.querySelectorAll('select.location-field'));
// const mapboxLocationInputs = Array.from(document.querySelectorAll('.mapbox-location-input'));
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
// let mapCenter = map.getCenter();
// returns {lng: x, lat: y}

/////////////////////////////////////
// autocomplete for location inputs
////////////////////////////////
const locationInputs = document.querySelectorAll('input.mapbox-location-input')

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

// code adapted from:
// https://jqueryui.com/autocomplete/#remote-jsonp
// which fails me
// for (let location of $('.mapbox-location-input')) {
//     location.autocomplete({
//         source: function(req, resp) {
//             $.ajax( {
//                 url: `{mapboxGeocodeApiBaseUrl}?token={mapboxgl.accessToken}`,
//                 dataType: "jsonp",
//                 data: {
//                     term.req.term
//                 },
//                 succes: function(data) {
//                     resp (data);
//                 }
//             });
//         },
//         minLength: 3,
//         select: function(evt, ui) {
//             location.value = ui.item.value
//         }
//     })
// }

