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