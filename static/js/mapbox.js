const mapLat = document.querySelector('#map-lat').innerText
const mapLng = document.querySelector('#map-lng').innerText
const mapZoom = document.querySelector('#map-zoom').innerText

mapboxgl.accessToken = 'pk.eyJ1Ijoia2luZ3RvciIsImEiOiJja3A2ZmdtNmwyaHBlMnZtd2xxMmJ3Z3ljIn0.YpzXxkn-7AwHzZpWapeFjQ';
var map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [mapLng, mapLat], // starting position [lng, lat]
    zoom: mapZoom // starting zoom
});
map.addControl(new mapboxgl.NavigationControl());
map.addImage()
// let mapCenter = map.getCenter();
// returns {lng: x, lat: y}

