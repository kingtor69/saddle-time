console.log('app.js');
const queryString = parseCurrentQueryString();
const routeDeleteButts = document.querySelectorAll('.route-delete');
const routeShowButts = document.querySelectorAll('.route-show');
const routeEditButts = document.querySelector('.routes-edit');

const loggedInUserId = $('#g-user') ? $('#g-user')[0].value : false;

const flashDiv = document.querySelector('#flashes');
if (document.querySelector('#error-table')) {
    const deleteMe = document.querySelector('#error-table');
    deleteMe.remove()
};

function displayErrors(errorObj) {
    const errorTable = document.createElement('table');
    errorTable.classList.add("table","error-table","table-striped")
    errorTable.id="error-table"
    for (let error in errorObj) {
        const errorTr = document.createElement('tr');
        const errorTds = [document.createElement('td'), document.createElement('td')];
        errorTds[0].classList.add('error-type')
        errorTds[1].classList.add('error-message')
        errorTds[0].innerText = error;
        errorTds[1].innerText = errorObj[error];
        for (let td of errorTds) {
            errorTr.appendChild(td);
        };
        errorTable.appendChild(errorTr);
    };
    flashDiv.appendChild(errorTable);
};

function selectTwo(jQueryElement) {
    jQueryElement.select2({
        minimumInputLength: 3,
        ajax: {
            url: '/api/location',
            datatype: JSON,
            processResults: function (data) {
                const formattedData = data.results.map(element => {
                    return {
                        id: element.id,
                        text: element.text
                    };
                });
                return {
                  results:formattedData
                };
              }
        },
    });
};

function updateUrl(queryAdditions, keepCurrent) {
    let queryString = "?";
    let query;
    keepCurrent ? query = parseCurrentQueryString() : query = {};
    for (let key of Object.keys(queryAdditions)) {
        query[key] = queryAdditions[key];
    };
    let i = 0;
    for (let key of Object.keys(query)) {
        if (i > 0) {
            queryString += "&"
        }
        queryString += `${key}=${query[key]}`
        i++;
    };
    let newurl = window.location.origin + window.location.pathname + `${queryString}`;
    window.history.pushState({path:newurl},'',newurl);
};

function parseCurrentQueryString() {
    const queryCurrent = new URLSearchParams(window.location.search);
    const queryObject = {};
    for (const [key, value] of queryCurrent) {
        queryObject[key] = value;
    };
    return queryObject;
};

function processAutocomplete(e, selector, id) {
    let prefix = id;
    let location = selector.select2('data')[0].text;
    let htmlId = selector.select2('data')[0].id;
    let lattitude = false;
    let longitude = true;
    let floatString = "";
    let floatStringDone = false;
    let lng = NaN;
    let lat = NaN;

    for (let char of htmlId) {
        if (floatStringDone) {
            if (longitude) {
                lng = parseFloat(floatString);
                floatString="";
                longitude = false;
                lattitude = true;
                floatStringDone = false;
            } else if (lattitude) {
                lat = parseFloat(floatString);
            }
        } else {
            if (char === "p") {
                // turn "p" into decimal place
                floatString += ".";
            } else if (char === "c") {
                // comma means the number is done
                floatStringDone = true;
            } else if ( isInteger(char) || char === "-" ) {
                // numbers and negative indication are important
                floatString += char;
            };
            // any other character is skipped
        };
    };

    localStorage.setItem('mapLng', lng);
    localStorage.setItem('mapLat', lat);
    localStorage.setItem('mapGeocode', [lat, lng]);
    if (localStorage['units']) {
        units = localStorage['units']
    };
    const queryAdditions = {};
    if (typeof id === "number") {
        localStorage.setItem(`${prefix}Location`, location);
        prefix = (parseInt)`loc-${id}`
        queryAdditions[`${cpId}-lat`] = lat;
        queryAdditions[`${cpId}-lng`] = lng;
        updateUrl(queryAdditions, true);
        return [false, lat, lng];
    };

    if (prefix === "weather") {
        queryAdditions.location = location;
        queryAdditions.latitude = lat;
        queryAdditions.longitude = lng;
        queryAdditions.units = units;
        updateUrl(queryAdditions, false);
        return [units, lat, lng];
    };
    return [false, false, false];
};

function parseCpId(elementId) {
    // returns parsed checkpoint ID if passed elementId is a valid geocode html ID
    // returns false if not
    let parsedId = "";
    let goTime = "wait"
    for (let char of elementId) {
        if (char === "-") {
            if (goTime === "wait"){
                goTime = "go";
            } else if (goTime === "go") {
                goTime = "going";
            } else if (goTime === "going") {
                parsedId += char;
                goTime = "gone";
            };
        } else if (goTime === "go" || goTime === "going") {
            parsedId += char;
        };
        if (goTime === "gone") {
            parsedId = parsedId.slice(0, (parsedId.length-1))
            return parsedId;
        };
    };
    return false;
};

function flashMessages(msg) {
    flashDiv.innerHTML = "";
    if (typeof msg === "object") {
        let msgsKeys = Object.keys(msg);
        const msgsCodes = ['info', 'success', 'danger', 'primary', 'secondary'];
        for (let key of msgsKeys) {
            newMsg = document.createElement('p');
            newMsg.innerHTML = ""
            if (msgsCodes.includes(key)) {
                newMsg.classList.add(`text-${key}`);
                newMsg.innerText = `${msg[key]}`
            } else {
                newMsg.classList.add('text-warning');
                newMsg.innerText = `${key}: ${msg[key]}`
            }
            flashDiv.appendChild(newMsg)
            flashDiv.appendChild(document.createElement('br'))
        }
    } else if (typeof msg === "array") {
        let textColor = "primary";
        let start = 0;
        if (msg[0] in msgCodes) {
            textColor = msg[0];
            start = 1;
        };
        for (let i=start; i<msg.length; i++) {
            newMsg = document.createElement('p');
            newMsg.innerHTML = "";
            newMsg.classList.add(`text-${textColor}`);
            newMsg.innerText = line;
            flashDiv.appendChild(newMsg);
            flashDiv.appendChild(document.createElement('br'));
        };
    } else {
        flashMessages({"info": msg});
    };
};

function dataFromQueryString() {
    // function adapted from https://stackoverflow.com/questions/2090551/parse-query-string-in-javascript
    // answer by https://stackoverflow.com/users/44852/tarik

    const query = window.location.search.substring(1);
    queryObject = {};
    let data = query.split('&');
    for (let i = 0; i < data.length; i++) {
        let datum = data[i].split('=');
        queryObject[decodeURIComponent(datum[0])] = decodeURIComponent(datum[1]);
    };
    return queryObject;
};

function isInteger(str) {
    let parsed = parseInt(str);
    if (isNaN(parsed)) {return false};
    return true;
};

function isCheckpointKey(key) {
    // return true if passed key (string) is formatted correctly for a checkpoint as either latitude or longitude
    let splitKey = key.split('-');
    if (!(parseInt(splitKey[0]) >= 0)) {
        return false;
    };
    if (splitKey[1] !== "lat" && splitKey[1] !== "lng") {
        return false;
    };
    return true;
};

async function deleteOrDont(evt, table) {
    const enteredName = evt.target[0].value;
    const username = evt.target[1].value;
    const userId = evt.target[2].value;
    try {
        if (enteredName === username) {
            const resp = await axios.delete(`/api/${table}/${userId}/delete`);
            return true;
        } else {
            return false;
        };
    } catch (e) {
        flashMessages(e);
        return false;
    };
};

if (routeDeleteButts) {
    for (let routeDelete of routeDeleteButts) {
        routeDelete.addEventListener('click', (e) => {
            e.preventDefault(e);
            const id = parseInt(routeDelete.id);
            deleteRoute(id);
        });
    };
};
    
if (routeShowButts) {
    for (let routeShow of routeShowButts) {
        routeShow.addEventListener('click', (e) => {
            e.preventDefault(e);
            const id = parseInt(routeShow.id);
            loadRoute(id);
        });
    };
};

if (routeEditButts) {
    for (let routeEdit of routeEditButts) {
        routeEdit.addEventListener('click', (e) => {
            e.preventDefault(e);
            const id = parseInt(routeEdit.id);
            editRoute(id);
        });
    };
};

async function deleteRoute(id) {
    const url = `/api/routes/${id}`
    let resp = await axios.delete(url);
    if ("delete" in resp.data) {
        flashMessages({"success": `You have successfully deleted route #${id}`});
        location.reload();
    } else {
        flashMessages({"info": `Something went wrong while deleting route #${id}. Odd, that.`})
    };

};