// selectTwo(checkpointLocations);
// console.log(checkpointLocations);
// let location;

// get current queryString data (app.js)
const routeData = parseCurrentQueryString();
const routeForm = document.querySelector('#route-form');

if (Object.keys(routeData).length < 1) {
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
        cpLatLng = processAutocomplete(evt, checkpointLocation, cpId);
        // this is not using the boolean part of the return, so ditch it:
        cpLatLng.shift();
        const routeDataLatLng = {};
        // routeDataLatLng[`cp${cpId}LatLng`] = cpLatLng;
        routeDataLatLng[`${cpId}LatLng`] = cpLatLng;
        addObjToLocalStorage('routeData', routeDataLatLng)
        // U R THERE (in that function)
        let storedData;
        if ('routeData' in localStorage) {
            let json = localStorage.getItem('routeData');
            storedData = JSON.parse(json);
            localStorage.removeItem('routeData');
        };
        for (let key in storedData) {
            routeDataLatLng[key] = storedData[key];
        };
        localStorage.setItem('routeData', JSON.stringify(routeDataLatLng));
        previewRoute();
        // store to localStorage
        // update URL

        // preview route from current data
    });
};

routeForm.addEventListener('submit', previewRoute());

async function previewRoute() {
    const routeData = dataFromQueryString();
    let url = '/api/routes/preview?'
    for (const key in routeData) {
        url += `${key}=${routeData[key]}&`
    };
    url = url.slice(0, -1);
    resp = await axios.get(url);
    if ("errors" in resp.data) {
        handleErrors (resp.data.errors);
    }
    else {
        console.log('got the preview data');
        console.log(resp.data);
    };
    let routes = {};
    if ("routes" in resp.data) {
        routes = resp.data.routes;
        console.log (routes);
    } else {
        handleErrors({"routing error": "No bicycle routes were found for these checkpoints. Please try something else."})
    }
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
        localStorage.setItem(key, JSON.stringify(valueObj))
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

