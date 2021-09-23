console.log('users.js');
const defaultLocationTd = document.querySelector('#default-location-autocomplete');
// defaultLocationSelector is declared in mapbox.js as a jQuery object

selectTwo(defaultLocationSelector);
defaultLocationSelector.change((evt) => {
    evt.preventDefault();
    console.log('elementid: ', defaultLocationSelector[0].id);
    cpId = parseCpId(defaultLocationSelector[0].id);
    // if (!cpId) {
    // this alert was popping up when it didn't seem there was anything wrong, so I just ditched it
    //     alert ('something went wrong with that location, please try again');
    // };
    cpLatLng = processAutocomplete(evt, defaultLocationSelector, cpId);
    // this is not using the boolean part of the return, so ditch it:
    cpLatLng.shift();
    const routeDataLatLng = {};
    routeDataLatLng[`${cpId}LatLng`] = cpLatLng;
    if (goodRouteData()) {
        // reloading page is refreshing map more efficiently than erasing old routes/checkpoints/&c.
        location.reload();
        // previewRoute();
    } else {
        handleErrors({"warning": "there is not enough valid route data to preview a route (within 'change' eventListener)"})
    }
});