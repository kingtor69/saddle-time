
const flashDiv = document.querySelector('#flashes');
flashDiv.innerHTML = '';

function displayErrors(errorObj) {
    const errorTable = document.createElement('table');
    errorTable.classList.add("table","error-table","table-striped")
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
        // dropdownParent: $('#weather-table'),
        minimumInputLength: 3,
        ajax: {
            url: '/api/location',
            datatype: JSON,
            processResults: function (data) {
                // console.log(data);
                const formattedData = data.results.map(element => {
                    return {
                        id: element.id,
                        text: element.text
                    };
                });
                // Transforms the top-level key of the response object from 'items' to 'results'
                return {
                  results:formattedData
                };
              }
        },
        // allowClear: true
    });
}


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
}

function parseCurrentQueryString() {
    const queryCurrent = new URLSearchParams(window.location.search);
    const queryObject = {};
    for (const [key, value] of queryCurrent) {
        queryObject[key] = value;
    };
    return queryObject;
}

function processAutocomplete(e, selector, id) {
    // variable definitions with autocomplete anddefault values
    let prefix = id;
    let location = selector.select2('data')[0].text;
    let htmlId = selector.select2('data')[0].id;
    let lattitude = false;
    let longitude = true;
    let floatString = "";
    let floatStringDone = false;
    let lng = NaN;
    let lat = NaN;

    // if (!prefix.startsWith('loc-cp')) {
    //     localStorage.setItem(`${prefix}Location`, location);
    // }

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
            if (char === "_") {
                // skip underscores
            } else if (char === "p") {
                // turn "p" into decimal place
                floatString += ".";
            } else if (char === "c") {
                // comma means the number is done
                floatStringDone = true;
            } else {
                // any other character is assumed to be a number
                floatString += char;
            };
        };
    };
    localStorage.setItem('mapLng', lng);
    localStorage.setItem('mapLat', lat);
    localStorage.setItem('mapGeocode', [lat, lng]);
    if (localStorage['units']) {
        units = localStorage['units']
    };
    const queryAdditions = {};
    // if id is a number, it's a checkpoint ID
    if (typeof id === "number") {
        localStorage.setItem(`${prefix}Location`, location);
        prefix = (parseInt)`loc-${id}`
        queryAdditions[`${cpId}-lat`] = lat;
        queryAdditions[`${cpId}-lng`] = lng;
        updateUrl(queryAdditions, true);
        return [false, lat, lng];
    };

    // if it's not a number, it was passed as a prefix variable:
    if (prefix === "weather") {
        queryAdditions.location = location;
        queryAdditions.latitude = lat;
        queryAdditions.longitude = lng;
        queryAdditions.units = units;
        updateUrl(queryAdditions, false);
        return [units, lat, lng];
    };
    // if (prefix.startsWith("loc-cp")) {
    //     debugger;
    //     const cpId = parseCpId(prefix);
    //     console.log(`parsed to ${cpId}`);
    //     queryAdditions[`${cpId}Lat`] = lat;
    //     queryAdditions[`${cpId}Lng`] = lng;
    //     updateUrl(queryAdditions, true);
    //     return [false, lat, lng];
    // };
    return [false, false, false];
}

function parseCpId(elementId) {
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
}

// started rabbitholing on this.... it can wait
function handleErrors(errsObj) {
    // flashDiv.innerHTML = "";
    // newError = document.createElement('p');
    // newError.innerHTML = 
    // if (err.isAxiosError) {
    //     newError.classList.add('text-info');
    //     newError.innerText = 

    console.log(errsObj)
}