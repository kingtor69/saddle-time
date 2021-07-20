const mapLat = parseFloat(document.querySelector('#map-lat').innerText);
const mapLng = parseFloat(document.querySelector('#map-lng').innerText);
const geocode = [mapLng, mapLat];
const mapZoom = document.querySelector('#map-zoom').innerText;
const mapboxGeocodeApiBaseUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
let firstTime = true;

// display mapbox:
mapboxgl.accessToken = 'pk.eyJ1Ijoia2luZ3RvciIsImEiOiJja3A2ZmdtNmwyaHBlMnZtd2xxMmJ3Z3ljIn0.YpzXxkn-7AwHzZpWapeFjQ';
var map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [mapLng, mapLat], // starting position [lng, lat]
    zoom: mapZoom // starting zoom
});
// ...with navigation controls:
map.addControl(new mapboxgl.NavigationControl());
// ...and a pointer in the middle for the current geocode
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

function geocodeFromLocation(location) {
    
}

///////////////////////////
// location autocomplete //
///////////////////////////
// using Select2
const mapboxLocationSelectors = $('select.mapbox-location-selector');
mapboxLocationSelectors.each(() => {
    mapboxLocationSelectors.select2({
        minimumInputLength: 3,
        ajax: {
            url: '/api/location',
            datatype: JSON
        },
        // allowClear: true
    });
})

// need to add class="mapbox-location-selector form-control" because apparently it goes away when select2 is turned on
// maybe because it's inside a Bootstrap "modal:"
// https://select2.org/troubleshooting/common-problems

