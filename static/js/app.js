const errorDiv = document.querySelector('#flashes');

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
    errorDiv.appendChild(errorTable);
};