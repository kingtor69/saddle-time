console.log('routes.js');
const routeData = parseCurrentQueryString();
const routeForm = document.querySelector('#route-form');
const newCheckpointButts = $('.new-checkpoint-button');
const routeSaveDiv = document.querySelector('#save-div')
const routePreviewButt = document.querySelector('#preview-route');
const deleteCheckpointButts = $('.checkpoint-delete');
const loginFromRoute = document.querySelector('#login-from-route');
const signupFromRoute = document.querySelector('#signup-from-route');
const routeSaveForm = document.querySelector('#route-save-form');

window.addEventListener('DOMContentLoaded', (event) => {
    if ('routeInProgress' in localStorage) {
        const routeJSON = localStorage.getItem('routeInProgress');
        const routeInProgress = JSON.parse(routeJSON);
        updateUrl(routeInProgress, false);
        localStorage.removeItem('routeInProgress');
    };
    if (goodRouteData()) {
        routePreviewButt.hidden = false;
        routeSaveDiv.hidden = false;
        previewRoute();
    };
});

if (loginFromRoute) {
    loginFromRoute.addEventListener('click', (e) => {
        e.preventDefault();
        const queryStringObject = parseCurrentQueryString();
        localStorage.setItem('routeInProgress', JSON.stringify(queryStringObject));
        location.href="/login?return=/routes/new"
    });
};

if (signupFromRoute) {
    signupFromRoute.addEventListener('click', (e) => {
        e.preventDefault();
        const queryStringObject = parseCurrentQueryString();
        localStorage.setItem('routeInProgress', JSON.stringify(queryStringObject));
        location.href="/users/signup?return=/routes/new"
    });
};

if (routeSaveForm) {
    routeSaveForm.addEventListener('submit', (e) => {
        e.preventDefault();
        let routeName = e.target[0].value;
        const displayMessage = {errors: {}};
        let routeData;
        let checkpointApiData;
        let cprsApiData;
        if (routeName.length > 0 && routeName.length <= 40) {
            routeData['name'] = routeName;
            routeApiData = organizeRouteData(routeData);
            route_id = saveRoute(routeApiData);
            if (route_id) {
                checkpointApiData = organizeCheckpointData(routeData, route_id);
                checkpointIds = saveCheckpoints(checkpointApiData);
            };
            if (checkpointIds) {
                cprsApiData = organizeCheckpointsRoutesData(checkpointApiData, route_id, checkpointIds);
                successOrError = saveCheckpointsRoutes(cprsApiData);
            };
        } else if (routeName.length > 0) {
            displayMessage.errors['info'] = "Route name can only be a maximum of 40 characters long. Please try a shorter name";
        };
        if ("success" in successOrError) {
            flashMessages(successOrError.success);
        } else if ("errors" in successOrError) {
            flashMessages(successOrError.errors);
        } else {
            flashMessages({"error error": "This was neither a success nor a failure. What gives?"});
        };
        displayMessage[successOrErrorKey] = successOrError[successOrErrorKey];
    });
};

for (let checkpointLocation of checkpointLocations) {
    selectTwo(checkpointLocation);
    checkpointLocation.change((evt) => {
        evt.preventDefault();
        console.log('elementid: ', checkpointLocation[0].id);
        cpId = parseCpId(checkpointLocation[0].id);
        cpLatLng = processAutocomplete(evt, checkpointLocation, cpId);
        cpLatLng.shift();
        const routeDataLatLng = {};
        routeDataLatLng[`${cpId}LatLng`] = cpLatLng;
        if (goodRouteData()) {
            location.reload();
        } else {
            flashMessages({"warning": "there is not enough valid route data to preview a route (within 'change' eventListener)"})
        };
    });
};

for (let newCheckpointButt of newCheckpointButts) {
    newCheckpointButt.addEventListener('click', (e) => {
        console.log('clicked on a button');
        console.log(newCheckpointButt);
        let buttId = newCheckpointButt.id;
        let splitId = buttId.split('-');
        let id = parseInt(splitId[2]);
        if (!(id >= 0)) {
            flashMessages({danger: "Something went wrong with that checkpoing button. Please refresh the page and try again. If that doesn't work, please rebuild your route. Sorry about that. We're working on it."});
        };
        let qString = parseCurrentQueryString();
        qString['new-id']=id;
        if (qString.cps) {
            // increase cps by 1 in qString if it's already there
            qString.cps ++;
        } else {
            // add cps=1 to qString if it isn't
            qString.cps = 1;
        };
        updateUrl(qString, false);
        location.reload();
    });
};

for (let deleteCheckpointButt of deleteCheckpointButts) {
    deleteCheckpointButt.addEventListener('click', (e) => {
        console.log(e)
    })
}

routePreviewButt.addEventListener('click', (e) => {
    e.preventDefault();
    if (goodRouteData()) {
        location.reload();
        // previewRoute();
    } else {
        flashMessages({"feed me more data": "there is not enough valid route data to preview a route (within 'submit' eventListener)"});
    };
});

async function previewRoute() {
    const queryData = dataFromQueryString();
    const routeData = {};
    for (let key in queryData) {
        if (isCheckpointKey(key)) {
            routeData[key] = queryData[key];
        };
    };
    let url = '/api/routes/preview?'
    for (const key in routeData) {
        url += `${key}=${routeData[key]}&`
    };
    url = url.slice(0, -1);
    try {
        resp = await axios.get(url);
    } catch (err) {
        console.error(err);
        flashMessages(err);
        return;
    };
    if ("errors" in resp.data) {
        flashMessages (resp.data.errors);
    } else if ("Errors" in resp.data) {
        flashMessages(resp.data.Errors);
    };

    try {
        let routes = resp.data.routes;
        let waypoints = resp.data.waypoints;
        displayRoutes(routes, waypoints);
    } catch {
        flashMessages({"info": "Please enter at least two valid checkpoints."})
    }
};

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

function goodRouteData() {
    // Check that query string has enough data to complete a route. Returns boolean.
    let data = parseCurrentQueryString();
    const dataKeys = Object.keys(data);
    // there must be at least 4 keys in a valid route
    if (dataKeys.length < 4) {
        return false;
    };
    dataKeys.sort();
    let checkpoints = 0;
    const dataKeysSplit = [];
    for (let key of dataKeys) {
        if (isCheckpointKey(key)) {
            numLatOrLng = key.split('-');
            dataKeysSplit.push(numLatOrLng);
        };
    };
    let cpKeysSplitIntTest;
    // only keep keys that start with an integer
    cpKeysSplitIntTest = dataKeysSplit.filter(splitKeyIntTest => isInteger(splitKeyIntTest[0]))
    let cpKeysSplit;
    // ...and that are either "lat" or "lng" after a "-"
    cpKeysSplit = dataKeysSplit.filter(splitKey => (splitKey[1] === "lat" || splitKey[1] === "lng"));
    
    // there should be exactly two of each checkpoint number (dataKeysSplit[i][0]), one "lat" and one "lng" (dataKeysSplit[i][1]);
    for (let i=0; i<dataKeysSplit.length; i+=2) {
        let thisKey = dataKeysSplit[i];
        let nextKey = dataKeysSplit[i+1];
        if (thisKey[0] !== nextKey[0]) {
            return false;
        };
        if ((thisKey[1] !== "lat" || nextKey[1] !== "lng") && (thisKey[1] !== "lng" || nextKey[1] !== "lat")) {
            return false;
        };
    };
    return true;
};

function displayRoutes(routes, checkpoints) {
    placeMarker("green", 0, checkpoints[0].location);
    placeMarker("red", 999, checkpoints[checkpoints.length-1].location);
    for (let i=1; i<checkpoints.length - 1; i++) {
        let color = checkpointColors[i % checkpointColors.length]
        placeMarker(color, i, checkpoints[i][1], checkpoints[i][0])
    }
    // add "preferred" flag to routes[0]
    routes[0]['preferred'] = true;
    // set "preferred" to false for the rest
    for (let i = 1; i < routes.length; i++) {
        routes[i]['preferred'] = false;
    };
    for (let i=routes.length - 1; i >= 0; i--) {
        drawRoute(routes[i], i);
    };
    for (let route of routes) {
        if (route.preferred) {
            units = parseUnits();
            processDistance(route, units);
            processElevationChange(route, units);
            showDirections(routeData);
        };
    };
};

function parseUnits() {
    let units = "imperial";
    const qString = parseCurrentQueryString();
    if ("units" in qString) {
        units = qString.units;
    };
    return units;
};

function convertDistance(meters, targetUnits) {
    // our APIs return distance and elevation data in meters
    // this function converts meters to km, feet or miles
    if (targetUnits === "kms") {
        return (meters/1000).toFixed(2);
    };
    if (targetUnits === "miles") {
        return (meters/1609).toFixed(1);
    };
    if (targetUnits === "feet") {
        return (meters*3.28).toFixed(0);
    }
    return meters;
};

function processDistance(route, units) {
    distanceUnits = units === "metric" ? "kms" : "miles";
    route['distanceUnits'] = distanceUnits;
    route.distance = convertDistance(route.distance, distanceUnits);
};

function processElevationChange(route, units) {
    // changes route object to include total elevation change
    // first does the calculations in meters
    const elevationObject = route.geometry.elevation;
    const elevationProfile = elevationObject.elevationProfile
    let elevationStart = elevationProfile[0].height;
    let elevationChange = 0;
    let totalClimbs = 0;
    let totalDescents = 0;
    for (let i = 1; i < elevationProfile.length; i++) {
        let thisStepsChange = elevationProfile[i].height - elevationStart;
        elevationChange = elevationChange + thisStepsChange;
        if (thisStepsChange > 0) {
            totalClimbs += thisStepsChange;
        } else if (thisStepsChange < 0) {
            totalDescents += thisStepsChange * -1;
        }
        elevationStart = elevationProfile[i].height
    };
    // now converts if needed
    let elevationUnits = "meters";
    if (units !== "metric") {
        elevationUnits = "feet";
        elevationChange = convertDistance(elevationChange, elevationUnits);
        totalClimbs = convertDistance(totalClimbs, elevationUnits);
        totalDescents = convertDistance(totalDescents, elevationUnits);
    };

    // and writes calculated values to route object
    route.geometry.elevation['totalElevationChange'] = elevationChange;
    route.geometry.elevation['totalClimbs'] = totalClimbs;
    route.geometry.elevation['totalDescents'] = totalDescents;
    route.geometry.elevation['elevationUnits'] = elevationUnits;
};

function showDirections(route) {
    const summaryDiv = document.querySelector('#summary');
    const summaryP = document.createElement('p');
    summaryP.innerHTML = `Total distance: ${route.distance} ${route.distanceUnits}<br>Elevation change: +${route.geometry.elevation.totalClimbs} ${route.geometry.elevation.elevationUnits}, -${route.geometry.elevation.totalDescents} ${route.geometry.elevation.elevationUnits}`;
    summaryDiv.appendChild(summaryP);
    const directionsDiv = document.querySelector('#directions');
    const directionsOl = document.createElement('ol');
    directionsOl.classList.add('pl-0', 'leg-list');
    for (let leg of route.legs) {
        const legLi = document.createElement('li');
        if (route.legs.length === 1) {
            legLi.classList.add('h4', 'py-2', 'single-leg')
        } else {
            legLi.classList.add('h4', 'py-2', 'leg-list');
        }
        legLi.innerText = leg.summary;
        directionsOl.appendChild(legLi);
        const stepOl = document.createElement('ol');
        stepOl.classList.add('pl-0');
        for (let step of leg.steps) {
            const stepLi = document.createElement('li');
            stepLi.classList.add('my-2');
            const stepButton = document.createElement('button');
            stepButton.classList.add('step-buttons', 'btn', 'btn-sm', 'btn-outline-info', 'py-1');
            stepButton.id = step.maneuver.location;
            stepButton.innerText = step.maneuver.instruction;
            stepLi.appendChild(stepButton);
            stepOl.appendChild(stepLi);
        };
        directionsOl.appendChild(stepOl);
    };
    directionsDiv.appendChild(directionsOl);
    const stepButtons = $('.step-buttons');
    for (let button of stepButtons) {
        button.addEventListener('click', (e) => {
            const stepLocation = button.id.split(',');
            reCenterMap(stepLocation);
        });
    };
};

function organizeRouteData(routeRawData) {
    // validate data
    const organizedRouteData = {user_id: loggedInUserId,
                                route_name: routeRawData.name};
    return {"route": organizedRouteData};
};

function organizeCheckpointData(routeRawData, route_id) {
    const organizedCheckpointArray = [];
    const checkpointKeys = [];
    for (let key in routeData) {
        if (isCheckpointKey(key)) {
            checkpointKeys.push(key);
        };
    };
    checkpointKeys.sort();
    for (let i=0; i<checkpointKeys.length; i = i+2) {
        organizedCheckpointArray.push({
            lat: routeRawData[checkpointKeys[i]],
            lng: routeRawData[checkpointKeys[i+1]],
            route_id: route_id,
            user_id: loggedInUserId
        });
    };
    return {"checkpoints": [organizedCheckpointsData]};
};

function organizeCheckpointsRoutesData(checkpointApiData, route_id, checkpointIds) {
    const organizedCheckpointRoutesArray = [];
    for (let i=0; i<checkpointIds.length; i++) {
        const newCpr = {
            route_id: route_id,
            checkpoint_id: checkpointIds[i],
            route_order: i
        };
        organizedCheckpointRoutesArray.push(newCpr);
    }
    return {"checkpointsRoutes": organizedCheckpointsRoutesArray};
};

async function saveRoute (routeObject) {
    let resp = await axios.post('/api/routes', JSON.stringify(routeObject));
    let routeData;
    if (!resp.data) {
        flashMessages({"danger": "the server sent no data back"});
    } else if (resp.data.errors) {
        flashMessages(resp.data.errors);
    } else {
        try {
            routeData=resp.data.route;
        } catch (e) {
            flashMessages(e);
            return false;
        };
    };
    try {
        return routeData.id
    } catch (e) {
        flashMessages(e);
        return false;
    }
};

async function saveCheckpoints (checkpointsArray) {
    const checkpointIds = []
    for (let checkpoint of checkpointsArray) {
        let resp = await axios.post('/api/checkpoitns', JSON.stringify(checkpoint));
        // validate response
        // push checkpointId to checkpointIds
    };
    return checkpointIds;
    // else error message
};

async function saveCheckpointsRoutes (cprArray) {
    for (let cpr of cprArray) {
        let resp = await axios.post('/api/checkpoints-routes', JSON.stringify(cpr));
        // validate response
    };
    // all good, return this:
    displayMe = "Route successfully saved."
    return {success: {info: displayMe}};
    // else return error message
    return {errors: {apiError: "something went wrong dude"}}
}