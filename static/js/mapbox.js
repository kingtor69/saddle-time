// This file contains code that is either directly from or lightly adapted from code in mapbox' docs (https://docs.mapbox.com)
console.log('mapbox.js');
let mapLat = defaultLoc_lat;
let mapLng = defaultLoc_lng;
const geocode = [mapLng, mapLat];
const mapZoom = document.querySelector('#map-zoom').innerText;
const mapboxGeocodeApiBaseUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
let firstTime = true;
const checkpointColors = ['yellow', 'pink', 'orange', 'purple'];
const checkpointFilename = "mapbox-marker-icon-20px-";

if (localStorage['mapLat'] && localStorage['mapLng']) {
    mapLat = localStorage['mapLat'];
    mapLng = localStorage['mapLng'];
};
if (parseFloat($('#map-lat').text()) && parseFloat($('#map-lng').text())) {
    mapLat = parseFloat(document.querySelector('#map-lat').innerText);
    mapLng = parseFloat(document.querySelector('#map-lng').innerText);
};

// display mapbox:
mapboxgl.accessToken = 'pk.eyJ1Ijoia2luZ3RvciIsImEiOiJja3A2ZmdtNmwyaHBlMnZtd2xxMmJ3Z3ljIn0.YpzXxkn-7AwHzZpWapeFjQ';
let map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [mapLng, mapLat], // starting position [lng, lat]
    zoom: mapZoom // starting zoom
});
// ...with navigation controls:
map.addControl(new mapboxgl.NavigationControl());
// ...and a pointer in the middle for the current geocode
map.on('load', function() {
    markerImg = "";
    color = "";
    const markerType = $('#marker').text();
    if (markerType === "urhere") {
        color = 'blue';
        markerImg = `${checkpointFilename}${color}.png`;
    } else if (markerType === "cp0") {
        color = 'green';
        markerImg = `${checkpointFilename}${color}.png`;
    } else if (!markerType || markerType.toLowerCase() === "none") {
        color = false;
        markerImg = false;
    } else {
        color = 'gray';
        markerImg = `${checkpointFilename}${color}.png`;
    }

    map.loadImage(`/static/images/mapbox-icons/${markerImg}`, function (error, image) {
        if (error) throw error;
        map.addImage(`${color}Pointer`, image);
        map.addSource('point', {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': [
                    {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': geocode
                        }
                    }
                ]
            }
        });
            
        map.addLayer({
            'id': 'points',
            'type': 'symbol',
            'source': 'point',
            'layout': {
                'icon-image': `${color}Pointer`,
                'icon-size': 1
            }
        });
    })
})

const weatherLocationSelector = $('#weather-selector');

const cpls = $('select.mapbox-location-selector');
const checkpointLocations = [];
for (let cpl of cpls) {
    const checkpointLocation = $(`#${cpl.id}`);
    checkpointLocations.push(checkpointLocation);
};

const defaultLocationSelector = $('default-location-selector')

function centerMap(lat, lng) {
    map.flyTo({
        center: [lng, lat]
    });
};

function placeMarker(color, id, lngLat) {
    console.log(`placeMarker(${color}, ${id}, ${lngLat})`)
    map.loadImage(`/static/images/mapbox-icons/${checkpointFilename}${color}.png`, function (error, image) {
        if (error) throw error;
        try {
            map.removeImage(`${id}Pointer`)
        } catch(err) {
            console.log(`no pointer with id ${id} exists... yet`)
        }
        map.addImage(`${id}Pointer`, image);
        map.addSource('point', {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': [
                    {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': lngLat
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
                'icon-image': `${id}Pointer`, // reference the image
                'icon-size': 1
            }
        });
    })
}


function drawRoute(routeData, index) {
    try {
        map.removeLayer(`line${index}`)
        map.removeSource(`route${index}`)
    } catch (err) {
        console.error(`no existing layer ${index} to remove`)
    }
    let color = '#aaa';
    if (routeData.preferred) {
        color = '#0080ff';
    };
    const routeCoordinates = routeData.geometry.coordinates

    map.addSource(`route${index}`, {
        'type': 'geojson',
        'data': {
            'type': 'Feature',
            'geometry': {
                'type': routeData.geometry.type,
                'coordinates': routeCoordinates
            }
        }
    });

    map.addLayer({
        'id': `line${index}`,
        'type': 'line',
        'source': `route${index}`,
        'layout': {},
        'paint': {
            'line-color': color,
            'line-width': 6
        }
    });
}

function reCenterMap(lngLat) {
    map.setCenter(lngLat);
    map.setZoom(16);
};