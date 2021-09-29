console.log('users.js');
const defaultLocationTd = document.querySelector('#default-location-autocomplete');
const userDeleteButt = document.querySelector('#user-delete');
const deleteConfirmation = document.querySelector('#delete-confirmation')
const userDeleteForm = document.querySelector('#user-delete-form');
const deleteCancelButt = document.querySelector('#delete-cancel');
const deleteUnconfirmed = document.querySelector('#delete-unconfirmed');
// defaultLocationSelector is declared in mapbox.js as a jQuery object;

userDeleteButt.addEventListener('click', (e) => {
    e.preventDefault();
    deleteUnconfirmed.hidden = true;
    deleteConfirmation.hidden = false;
});

deleteCancelButt.addEventListener('click', (e) => {
    e.preventDefault();
    deleteConfirmation.hidden = true;
    deleteUnconfirmed.hidden = false;
});

userDeleteForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (deleteOrDont(e, 'users')) {
        location.href='/logout?deleted=true';
    } else {
        const deleteWarning = document.querySelector('#delete-warning');
        deleteWarning.innerText = "That was not correct. Please try entering your username again or cancel.";
    };
});

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
        flashMessages({"warning": "there is not enough valid route data to preview a route (within 'change' eventListener)"})
    }
});