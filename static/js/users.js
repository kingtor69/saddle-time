console.log('users.js');
const defaultLocationTd = document.querySelector('#default-location-autocomplete');
// defaultLocationSelector is declared in mapbox.js as a jQuery object

selectTwo(defaultLocationSelector);
defaultLocationSelector.change((evt) => {
    evt.preventDefault();
    console.log('elementid: ', defaultLocationSelector[0].id);
    cpId = parseCpId(defaultLocationSelector[0].id);
    cpLatLng = processAutocomplete(evt, defaultLocationSelector, cpId);
    cpLatLng.shift();
    const routeDataLatLng = {};
    routeDataLatLng[`${cpId}LatLng`] = cpLatLng;
    if (goodRouteData()) {
        location.reload();
        previewRoute();
    } else {
        handleErrors({"warning": "there is not enough valid route data to preview a route (within 'change' eventListener)"})
    }
});