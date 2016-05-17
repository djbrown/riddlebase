RiddleManager = (function () {

    const RIDDLE_CELL_SIZE = 30;
    const PICKER_CELL_SIZE = 25;
    const OFFSET = 2;
    const DEFAULT_ZOOM_FACTOR = 1.4;
    var zoomFactor = 1;

    function init() {
        var zoomDelta = 0.2;

        $("#shrink").click(createSetZoomDeltaFunction(-zoomDelta));
        $("#restore-size").click(resetZoom);
        $("#enlarge").click(createSetZoomDeltaFunction(zoomDelta));
        $("#full-screen").click(toggleFullScreen);
    }

    function adjustViewBox() {
        var svg = document.getElementById("riddle");
        //noinspection JSUnresolvedFunction
        var bBox = svg.getBBox();

        var x = -OFFSET;
        var y = -OFFSET;
        var width = bBox.width + 2 * OFFSET;
        var height = bBox.height + 2 * OFFSET;
        var viewBox = x + " " + y + " " + width + " " + height;

        svg.setAttribute("viewBox", viewBox);
    }

    function applyZoom() {
        document.getElementById("full-screen").classList.remove("active");
        var svg = document.getElementById("riddle");
        svg.classList.remove("full-screen");
        //noinspection JSUnresolvedFunction
        var bBox = svg.getBBox();

        var width = bBox.width + 2 * OFFSET;
        var svgWidth = width * zoomFactor;

        svg.setAttribute("width", svgWidth.toString());
    }

    function createSetZoomDeltaFunction(zoomDelta) {
        return function () {
            setZoomFactor(zoomFactor += zoomDelta);
        };
    }

    function resetZoom() {
        setZoomFactor(DEFAULT_ZOOM_FACTOR);
    }

    function toggleFullScreen() {
        var svg = document.getElementById("riddle");
        svg.classList.toggle("full-screen");
        document.getElementById("full-screen").classList.toggle("active");
    }

    function setZoomFactor(newZoomFactor) {
        if (newZoomFactor < 0) {
            return;
        }
        zoomFactor = newZoomFactor;
        applyZoom();
    }

    function createSvgElement(qualifiedName) {
        return document.createElementNS("http://www.w3.org/2000/svg", qualifiedName);
    }

    function check(proposal, correctFallbackFunction) {
        var ajax = new XMLHttpRequest();
        ajax.onreadystatechange = function () {
            if (ajax.readyState == 4 && ajax.status == 200) {
                var response = JSON.parse(ajax.responseText);
                if (response.correct === true) {
                    correctFallbackFunction();
                }
            }
        };
        ajax.open("POST", "check/", true);
        ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        ajax.send("proposal=" + proposal);
    }

    return {
        RIDDLE_CELL_SIZE: RIDDLE_CELL_SIZE,
        PICKER_CELL_SIZE: PICKER_CELL_SIZE,
        init: init,
        resetZoom: resetZoom,
        adjustViewBox: adjustViewBox,
        createSvgElement: createSvgElement,
        check: check
    };
})();
