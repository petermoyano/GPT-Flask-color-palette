const form = document.querySelector("#form");

document.addEventListener("DOMContentLoaded", function () {
    getColors();
});

form.addEventListener("submit", function (e) {
    e.preventDefault();
    disableButtonOnSubmit();
    getColors();
});
