const btn = document.querySelector('#confirm');
btn.addEventListener('click', (event) => {
    getSelectedCheckboxValues('item');
});

function getSelectedCheckboxValues(name) {
    const checkboxes = document.querySelectorAll(`input[name="${name}"]:checked`);
    let values = [];
    checkboxes.forEach((checkbox) => {
        values.push(checkbox.value);
    });
    return values;
}