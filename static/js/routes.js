const routeForm = document.querySelector('#route-form');
const checkpointForms = document.querySelectorAll("[id^='cpf-']");
const checkpointFormsArray = Array.from(checkpointForms);
const checkpointNumbers = [];
for (let i = 0; i < checkpointFormsArray.length; i++) {
    const thisId = checkpointFormsArray[i].id;
    let formIndex = ""
    numberOn = false
    for (let i = 0; i < thisId.length; i++) {
        if (numberOn || thisId[i-1] === "-") {
            numberOn = true
            formIndex += thisId[i]
        }
    }
    checkpointNumbers[i] = parseInt(formIndex);
};
// aw, jeez, I gots to get the mapping autocomplete thing done before I can do this.....
checkpointLocations = []
for (let checkpointId of checkpointNumbers) {

}
// const documentFields = document.querySelectorAll('.form-field')
// console.log(documentFields)

routeForm.addEventListener('submit', function(e) {
    e.preventDefault();
    // const routeFormTarget = e.target;
    const routeInfo = getRouteInfo();

    if (checkpointNumbers.length < 2) {
        throw new Error('A route needs at least 2 checkpoints.')
    } else if (checkpointNumbers.length === 2) {
        routeInfo.routeSegments = "";
    } else {
        routeInfo.routeSegments = [];
        for (let i = 0; i < (checkpointNumbers.length - 1); i++) {
            routeInfo.routeSegments[i] = await setRouteSegment(checkpoint)
        }
    }

    console.log (routeInfo)
});

function getRouteInfo() {
    // retrieves route info basics (route name, bike type) from form
    const routeInfo = {};
    routeFields = routeForm.querySelectorAll('.form-field');
    const routeFieldsArray = Array.from(routeFields);
    for (let i = 0; i < routeFieldsArray.length; i++) {
        routeInfo[routeFields[i].id] = routeFields[i].value
    };
    return routeInfo;
}

async function getRouteSegment(locA, locB) {
    // takes start and end point locations returns geocodes for that route segment in this formal: 
    // [[lattitudeA, longitudeA], [lattitudeB, longitudeB]]
    const geocodeA = await getGeocode(locA);
    const geocodeB = await getGeocode(locB);
    return [geocodeA, geocodeB]
}

async function getGeocode(location) {
    const geocode = await axios.get(`/api/`)
    return geocode;
}