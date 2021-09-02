// get current queryString data (app.js)
const routeData = parseCurrentQueryString();
const routeForm = document.querySelector('#route-form');

// maybe ditch this next bit
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
        routeDataLatLng[`${cpId}LatLng`] = cpLatLng;
        // I don't think I'm using, or need to use, localStorage.routeData right now for checkpoints' geocodes
        // i.e. there's probably some useless code around here
        addObjToLocalStorage('routeData', routeDataLatLng)
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
        if (goodRouteData()) {
            let routes = previewRoute();
            displayRoutes(routes);
        }
        // store *this* to localStorage?
    });
};

routeForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (goodRouteData()) {
        previewRoute();
    } else {
        handleErrors({"feed me more data": "there is not enough valid route data to preview a route"})
    }
});

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
        return routes;
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

function goodRouteData() {
    // Check that query string has lat and lng for 2 or more checkpoints. Returns boolean.
    let data = parseCurrentQueryString();
    let dataKeys = Object.keys(data);
    let checkpoints = 0;
    for (let i = 0; i < dataKeys.length; i++) {
        // if key does NOT start with a number, it's not a checkpoint
        if (parseInt(dataKeys[i])) {
            // do we have two of the same number in a row?
            if (i > 0 && parseInt(dataKeys[i] === parseInt(dataKeys[i-1]))) {
                // finally, does that pair of keys each contain one of "lat" and "lng" (in either order)
                if (("lat" in dataKeys[i] && "lng" in dataKeys[i-1]) || "lng" in dataKeys[i] && "lat" in dataKeys[i-1]) {
                    // OK, that's a valid checkpoint
                    checkpoints ++
                }
            }
        }
    }
    if (checkpoints >= 2) {
        return true;
    }
    return false;
}