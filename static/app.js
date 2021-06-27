const errorDiv = document.querySelector('#errors');

function displayErrors(errorArr) {
    console.log(`displayErrors(${errorArr})`)
    const errorTable = document.createElement('table');
    errorTable.classList.add("table","table-danger","table-striped")
    for (let error of errorArr) {
        const errorTr = document.createElement('tr');
        const errorTds = [document.createElement('td'), document.createElement('td')];
        errorTds[0].innerText = error[0];
        errorTds[0].innerText = error[1];
        for (let td of errorTds) {
            errorTr.appendChild(td);
        };
        errorTable.appendChild(errorTr);
    };
    errorDiv.appendChild(errorTable);
};