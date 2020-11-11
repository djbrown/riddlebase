export const RIDDLE_CELL_SIZE = 30;
export const PICKER_CELL_SIZE = 25;
const OFFSET = 2;
const DEFAULT_ZOOM_FACTOR = 1.4;

let zoomFactor = 1;

function applyZoom() {
    document.getElementById("full-screen").classList.remove("active");
    const svg = document.getElementById("riddle");
    svg.classList.remove("full-screen");
    //noinspection JSUnresolvedFunction
    const bBox = svg.getBBox();

    const width = bBox.width + 2 * OFFSET;
    const svgWidth = width * zoomFactor;

    svg.setAttribute("width", svgWidth.toString());
}

function setZoomFactor(newZoomFactor) {
    if (newZoomFactor < 0) {
        return;
    }
    zoomFactor = newZoomFactor;
    applyZoom();
}

export function resetZoom() {
    setZoomFactor(DEFAULT_ZOOM_FACTOR);
}

function createSetZoomDeltaFunction(zoomDelta) {
    return function () {
        setZoomFactor(zoomFactor += zoomDelta);
    };
}

function toggleFullScreen() {
    const svg = document.getElementById("riddle");
    svg.classList.toggle("full-screen");
    document.getElementById("full-screen").classList.toggle("active");
}

function initUserControls() {
    // TODO: init user controls (save, restore, comment, rate)
}

export function init() {
    const zoomDelta = 0.2;

    document.getElementById("shrink").addEventListener("click", createSetZoomDeltaFunction(-zoomDelta));
    document.getElementById("enlarge").addEventListener("click", createSetZoomDeltaFunction(zoomDelta));
    document.getElementById("restore-size").addEventListener("click", resetZoom);
    document.getElementById("full-screen").addEventListener("click", toggleFullScreen);

    if (document.getElementById("save") !== null) {
        initUserControls();
    }
}

export function adjustViewBox() {
    const svg = document.getElementById("riddle");
    //noinspection JSUnresolvedFunction
    const bBox = svg.getBBox();

    const x = -OFFSET;
    const y = -OFFSET;
    const width = bBox.width + 2 * OFFSET;
    const height = bBox.height + 2 * OFFSET;

    svg.setAttribute("viewBox", `${x} ${y} ${width} ${height}`);
}

export function createSvgElement(qualifiedName) {
    return document.createElementNS("http://www.w3.org/2000/svg", qualifiedName);
}

export function check(state, correctFallbackFunction) {
    const ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function () {
        if (ajax.readyState === 4 && ajax.status === 200) {
            const response = JSON.parse(ajax.responseText);
            if (response.correct === true) {
                correctFallbackFunction();
            }
        }
    };
    ajax.open("POST", "check/", true);
    ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    ajax.send(`state=${state}`);
}
