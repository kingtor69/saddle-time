// selectTwo(checkpointLocations);
// console.log(checkpointLocations);
// let location;

// get current queryString data
const queryString = new URLSearchParams(window.location.search);
let routeData = Object.fromEntries(queryString.entries());

if (routeData.length < 1) {
    // if queryString is empty, check for current data from localStorage 
    if ('routeData' in localStorage) {
        routeData = localStorage.routeData;
    };
} else {
    // if not, replace localStorage with queryString data
    localStorage.removeItem('routeData');
    localStorage.setItem('routeData', JSON.stringify(routeData));
};

for (let checkpointLocation of checkpointLocations) {
    selectTwo(checkpointLocation);
    // if (checkpointLocation.select2('data')[0].text) {
    //     location = checkpointLocation.select2('data')[0].text
    // }
    // checkpointIndex = parseIdForCpIndex(location.id)
    checkpointLocation.change((evt) => {
        evt.preventDefault();
        console.log('elementid: ', checkpointLocation[0].id);
        cpId = parseCpId(checkpointLocation[0].id);
        if (!cpId) {
            alert ('something went wrong with that location, please try again');
        };
        console.log('cpid: ', cpId);
        cpLatLng = processAutocomplete(evt, checkpointLocation, `loc-${checkpointLocation[0].id}`);
        cpLatLng.shift();
        const routeDataLatLng = {};
        routeDataLatLng[`cp${cpId}LatLng`] = cpLatLng;
        addObjToLocalStorage('routeData', routeDataLatLng)
        // U R THERE (in that function)
        if (!'routeData' in localStorage) {
            localStorage.setItem('routeData', '')
        }
        // store to localStorage
        // update URL

        // preview route from current data

    })
}

// prepare checkpoint markers with 4 rotating colors for intermediate checkpoints
const checkpointMarkers = [`%{checkpointFilename}green.png`]
for (let i=1; i < (checkpointLocations.length - 1); i++) {
    checkpointMarkers[i] = `${checkpointFilename}${checkpointColors[(i%checkpointColors.length)-1]}.png`
};

function parseCpId (selectorId) {
    // gets ID number (integer) from selector ID when format is {prefix}-{id#}-{suffix}. Returns false if an ID is not found.
    let gotIt = false;
    let id = "";
    for (let char of selectorId) {
        if (char === "-") {
            if (!gotIt) {
                gotIt = true;
            } else {
                return parseInt(id);
            }
        } else if (gotIt) {
            id += char;
        }
    }
    return false;
};

function addObjToLocalStorage(key, valueObj) {
    if (key in localStorage) {
        let currentValue = JSON.parse(localStorage[key]);
        // U R HERE: untested
        if (typeof currentValue === "object") {
            for (let key in valueObj) {
                currentValue[key] = valueObj[key]
            };
            return;
        } 
        throw new Error;
    } else {
        localStorage.setItem(key, value)
        return;
    }
}

// pre-populating the "start" checkpoint (cp0) is happening in PythonFlask now, and I think that's why I started all this
// for (let locator of $('select.checkpoint-location')) {
//     selectTwo(locator);
// }

// $('#cp-0-')

// if ($('#map-lat') && $('#map-lng')) {

// };

// async function reverseGeocode(lat, lng) {
//     resp = await axios.get(`/api/location?lat=${lat}&lng=${lng}`)
//     console.log(resp)
// };

