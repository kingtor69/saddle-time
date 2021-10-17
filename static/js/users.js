const defaultLocationTd = document.querySelector('#default-location-autocomplete');
selectTwo(defaultLocationSelector);
defaultLocationSelector.change((evt) => {
    evt.preventDefault();
    cpId = parseCpId(defaultLocationSelector[0].id);
    cpLatLng = processAutocomplete(evt, defaultLocationSelector, cpId);
    cpLatLng.shift();
    const routeDataLatLng = {};
    routeDataLatLng[`${cpId}LatLng`] = cpLatLng;
    if (goodRouteData()) {
        location.reload();
        previewRoute();
    } else {
        flashMessages({"warning": "there is not enough valid route data to preview a route (within 'change' eventListener)"})
    }
});