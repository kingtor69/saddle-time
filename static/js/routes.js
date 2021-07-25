selectTwo(checkpointLocations);

if ($('#map-lat') && $('#map-lng')) {
    
};

const checkpointMarkers = [`%{checkpointFilename}green.png`]
for (let i=1; i < (checkpointLocations.length - 1); i++) {
    checkpointMarkers[i] = `${checkpointFilename}${checkpointColors[(i%checkpointColors.length)-1]}.png`
};

async function reverseGeocode(lat, lng) {
    resp = await axios.get(`/api/location`)
};

// for (let locator of $('select.checkpoint-location')) {
//     selectTwo(locator);
// }

// $('#cp-0-')