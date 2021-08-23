
const flashDiv = document.querySelector('#flashes');

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
    let queryCurrent;
    keepCurrent ? queryCurrent = parseCurrentQueryString() : queryCurrent = []
    console.log(queryCurrent)
    queries = [...queryCurrent, ...queryAdditions];
    for (let i = 0; i < queries.length; i++) {
        if (i > 0) {
            queryString += "&"
        }
        queryString += `${queryAdditions[i][0]}=${queryAdditions[i][1]}`
    }
    let newurl = window.location.origin + window.location.pathname + `${queryString}`;
    window.history.pushState({path:newurl},'',newurl);
}

function parseCurrentQueryString() {
    const queryCurrent = [];
    return queryCurrent;
}

function processAutocomplete(e, selector, prefix) {
    console.log(`app.js processAutocomplete prefix=${prefix}`)

    let location = selector.select2('data')[0].text;
    if (!prefix.startsWith('loc-cp')) {
        localStorage.setItem(`${prefix}Location`, location);
    }
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
        }
    }
    localStorage.setItem('mapLng', lng);
    localStorage.setItem('mapLat', lat);
    localStorage.setItem('mapGeocode', [lat, lng]);
    if (localStorage['units']) {
        units = localStorage['units']
    };
    const queryAdditions = [];
    if (prefix === "weather") {
        queryAdditions.push(['location', location]);
        queryAdditions.push(['latitude', lat]);
        queryAdditions.push(['longitude', lng]);
        queryAdditions.push(['units', units]);
        updateUrl(queryAdditions, false);
        return [units, lat, lng];
    };
    if (prefix.startsWith("loc-cp")) {
        const cpId = parseCpId(prefix);
        console.log(`parsed to ${cpId}`);
        queryAdditions.push[`${cpId}Lat`, lat];
        queryAdditions.push[`${cpId}Lng`, lng];
        updateUrl(queryAdditions, true);
        return [false, lat, lng];
    };
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