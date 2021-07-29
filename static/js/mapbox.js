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
    // possible future development: 
    // use integers for marker
    // 1000 = blue (urhere)
    // 0 = green
    // 999 = red
    // odd = yellow
    // even = orange
    if ($('#marker').text() === "urhere") {
        markerImg = `${checkpointFilename}blue.png`;
    } else if ($('#marker').text() === "cp0") {
        markerImg = `${checkpointFilename}green.png`;
    } else {
        markerImg = `${checkpointFilename}gray.png`;
    }

    map.loadImage(`/static/images/mapbox-icons/${markerImg}`, function (error, image) {
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
                            'coordinates': geocode
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

const weatherLocationSelector = $('#weather-selector');
const checkpointLocations = $('select.mapbox-location-selector')
// $('.location-field')

// console.log (`here we are with some locators`);
// console.log($('.location-field'));
// for (let locator of $('.location-field')) {
//     console.log(locator);
// };
