const addedCheckpointsSpan = document.querySelector('#added-checkpoints')
const newCheckpointRow = document.createElement('div');
newCheckpointRow.classList.add('row', 'justify-content-center', 'checkpoint-rows')
// const arrowsCol = document.createElement('div');
// arrowsCol.classList.add('col', 'col-1');
// const upArrowButton = document.createElement('button');
// upArrowButton.classList.add('arrows');
// const upArrowI = document.createElement('i');
// upArrowI.classList.add('far', 'fa-arrow-alt-circle-up');
// const downArrowButton = document.createElement('button');
// const downArrowI = document.createElement('i');
// downArrowI.classList.add('far', 'fa-arrow-alt-circle-down');
const addCheckpointCol = document.createElement('div');
addCheckpointCol.classList.add('col', 'col-11');
const addCheckpointButton = document.createElement('button');
addCheckpointButton.classList.add('btn', 'btn-secondary', 'btn-sm', 'add-cp-button');
addCheckpointButton.id = "new-checkpoint";
addCheckpointButton.innerText = "add checkpoint";

// upArrowButton.appendChild(upArrowI);
// downArrowButton.appendChild(downArrowI);

// arrowsCol.appendChild(upArrowButton);
// arrowsCol.appendChild(downArrowButton);
addCheckpointCol.appendChild(addCheckpointButton)

// newCheckpointRow.appendChild(arrowsCol);
addCheckpointArrows(newCheckpointRow);
newCheckpointRow.appendChild(addCheckpointCol);

addedCheckpointsSpan.appendChild(newCheckpointRow)

function addCheckpointArrows(column) {
    const arrowsCol = document.createElement('div');
    arrowsCol.classList.add('col', 'col-1');
    const upArrowButton = document.createElement('button');
    upArrowButton.classList.add('arrows');
    const upArrowI = document.createElement('i');
    upArrowI.classList.add('far', 'fa-arrow-alt-circle-up');
    const downArrowButton = document.createElement('button');
    downArrowButton.classList.add('arrows');
    const downArrowI = document.createElement('i');
    downArrowI.classList.add('far', 'fa-arrow-alt-circle-down');

    upArrowButton.appendChild(upArrowI);
    downArrowButton.appendChild(downArrowI);
    
    arrowsCol.appendChild(upArrowButton);
    arrowsCol.appendChild(downArrowButton);

    column.appendChild(arrowsCol);
};

const newCheckpointDiv = `
    <div class="row justify-content-center checkpoint-rows checkpoint-rows" id="cpr-{{index}}-row">
        <div class="col col-1">
            <button class="arrows"><i class="far fa-arrow-alt-circle-up"></i></button>
            <button class="arrows"><i class="far fa-arrow-alt-circle-down"></i></button>
        </div>
        <div class="col col-11">
            <button class="btn btn-secondary btn-sm d-inline-block mt-2" id="new-checkpoint">add checkpoint</button>
        </div>
    </div>

`

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
            routeInfo.routeSegments[i] = setRouteSegment(checkpoint)
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

async function setRouteSegment(checkpoint) {
    // TODO: this
}