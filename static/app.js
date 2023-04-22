const form = document.querySelector("#form");
form.addEventListener("submit", function (e) {
    e.preventDefault();
    getColors();
});

function getColors() {
    const query = form.elements.query.value;
    fetch("/palette", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
            query: query,
        }),
    })
        .then((response) => response.json()) //parse as json
        .then((data) => {
            const colors = data.colors;
            const container = document.querySelector(".container");
            createColoredBoxes(colors, container);
        });
}

function createColoredBoxes(colors, parent) {
    parent.innerHTML = "";
    for (const color of colors) {
        const div = document.createElement("div");
        div.style.backgroundColor = color;
        div.classList.add("color");
        div.style.width = `calc(100%/${colors.length})`;
        div.addEventListener("click", function () {
            navigator.clipboard.writeText(color);
        });
        const span = document.createElement("span");
        div.appendChild(span);
        span.innerText = color;
        parent.appendChild(div);
    }
}
