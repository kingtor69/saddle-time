const flashDiv = document.querySelector('#flashes');

function displayErrors(errorObj) {
    console.log(errorObj)
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

function updateUrl(queryString) {
    let newurl = window.location.origin + window.location.pathname + `?${queryString}`;
    window.history.pushState({path:newurl},'',newurl);
}

function processAutocomplete(e, selector, prefix) {
    let location = selector.select2('data')[0].text;
    localStorage.setItem(`${prefix}Location`, location);
    let htmlId = selector.select2('data')[0].id;
    let lattitude = false;
    let longitude = true;
    let floatString = "";
    let floatStringDone = false;
    let mapLng = NaN;
    let mapLat = NaN;
    for (let char of htmlId) {
        if (floatStringDone) {
            if (longitude) {
                mapLng = parseFloat(floatString);
                floatString="";
                longitude = false;
                lattitude = true;
                floatStringDone = false;
            } else if (lattitude) {
                mapLat = parseFloat(floatString);
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
    localStorage.setItem('${prefix}Lng', mapLng);
    localStorage.setItem('${prefix}Lat', mapLat);
    localStorage.setItem('${prefix}Geocode', [mapLat, mapLng]);
    if (localStorage['units']) {
        units = localStorage['units']
    };
    updateUrl(`location=${location}&latitude=${mapLat}&longitude=${mapLng}&units=${units}`);
    return [units [mapLat, mapLng]];
}