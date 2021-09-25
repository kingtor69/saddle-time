console.log(`hideMysteryTables.js`);

window.addEventListener('DOMContentLoaded', (event) => {
    const tables = document.querySelectorAll('table');
    for (let table of tables) {
        if (table.classList.length === 0) {
            table.hidden = true;
        };
    };
});