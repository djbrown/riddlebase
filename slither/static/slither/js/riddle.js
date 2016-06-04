var RiddleManager;

var Riddle = (function () {

    function createBorderClickFunction(row, column) {
        return function () {
            var picker = document.getElementById("picker");
            var pickerIsOpen = !picker.classList.contains("hide");

            if (select) {
                endSelection();
            }
            var isClosing = select === this && pickerIsOpen;
            if (!isClosing) {
                select = this;
                startSelection(row, column);
            }
        };
    }

    function addIndicator(parent, value, x, y, id, classNames) {
        var indicator = RiddleManager.createSvgElement("text");
        indicator.setAttribute("id", id);
        indicator.setAttribute("x", x);
        indicator.setAttribute("y", y);

        classNames.forEach(function (className) {
            indicator.classList.add(className);
        });

        var textNode = document.createTextNode(value);
        indicator.appendChild(textNode);

        parent.appendChild(indicator);
    }

    function addRiddleCell(pattern, state, row, column, numbers) {
        var indicatorsGroup = document.getElementById("riddle-indicators");

        var cell = RiddleManager.createSvgElement("g");
        cell.classList.add("riddle-cell");

        var size = RiddleManager.RIDDLE_CELL_SIZE;
        var x = size * column;
        var y = size * row;
        var transform = "translate(" + x + ", " + y + ")";
        cell.setAttribute("transform", transform);

        var classNames = ["value", "riddle-cell-value"];

        var value = pattern[row * numbers + column];
        if (value === "-") {
            value = state[row * numbers + column];
            classNames.push("state");
            cell.classList.add("state");
            if (value === "-") {
                value = "";
            }
        } else {
            classNames.push("pattern");
            cell.classList.add("pattern");
        }

        addRect(cell, 0, 0, size, size, ["riddle-cell-background"]);

        var textX = size / 2;
        var textY = size / 2;
        var id = "riddle-value-" + row + "-" + column;
        addIndicator(cell, value, textX, textY, id, classNames);

        if (classNames.indexOf("state") !== -1) {
            var riddleCellClickFunction = createBorderClickFunction(row, column);
            cell.addEventListener("click", riddleCellClickFunction);
        }

        indicatorsGroup.appendChild(cell);
    }

    function createIndicators(indicators, breadth) {
        var diagonale = breadth * 2 - 1;
        for (var row = 0; row < diagonale; row++) {
            var columns = breadth + row;
            for (var column = 0; column < columns; column++) {
                addRiddleCell();
            }
            columns++;
        }
    }

    function addBorder(parent, x, y, size, orientation, isBold, classNames) {
        var border = RiddleManager.createSvgElement("line");
        border.setAttribute("stroke-linecap", "square");

        border.classList.add("border");
        classNames.forEach(function (className) {
            border.classList.add(className);
        });
        if (isBold) {
            border.classList.add("bold");
        }

        var x2 = x;
        var y2 = y;
        if (orientation === "h") {
            x2 += size;
        } else if (orientation === "v") {
            y2 += size;
        } else {
            throw "Invalid border orientation: '" + orientation + "'" + " (expected 'h' or 'v'";
        }

        border.setAttribute("x1", x);
        border.setAttribute("y1", y);
        border.setAttribute("x2", x2);
        border.setAttribute("y2", y2);

        parent.appendChild(border);
    }

    function createRiddleGridRow(numbers, size, row, boxColumns, boxRows, gridBold, gridThin, classNames) {
        var y = size * row;
        for (var column = 0; column < numbers; column++) {
            var x = size * column;

            var isVBoxBorder = column % boxColumns === 0;
            var isHBoxBorder = row % boxRows === 0;

            var vGrid = isVBoxBorder ? gridBold : gridThin;
            var hGrid = isHBoxBorder ? gridBold : gridThin;

            addBorder(vGrid, x, y, size, "v", isVBoxBorder, classNames);
            addBorder(hGrid, x, y, size, "h", isHBoxBorder, classNames);
        }
        // create rightmost vertical border
        addBorder(gridBold, size * numbers, y, size, "v", true, classNames);
    }

    function createGrid(numbers, boxRows, boxColumns) {
        var gridThin = document.getElementById("riddle-grid-thin");
        var gridBold = document.getElementById("riddle-grid-bold");

        var size = RiddleManager.RIDDLE_CELL_SIZE;
        var classNames = [];

        for (var row = 0; row < numbers; row++) {
            createRiddleGridRow(numbers, size, row, boxColumns, boxRows, gridBold, gridThin, classNames);
        }
        // create lowest horizontal borders
        for (var column = 0; column < numbers; column++) {
            var lastRowBorderX = size * column;
            var lastRowBorderY = size * numbers;
            addBorder(gridBold, lastRowBorderX, lastRowBorderY, size, "h", true, classNames);
        }
    }

    function showWinningAnimation() {
        var backgrounds = document.getElementsByClassName("riddle-cell-background");
        for (var i = 0; i < backgrounds.length; i++) {
            backgrounds[i].classList.add("winning");
        }
    }

    function propose() {
        var proposal = "";
        var cellValues = document.getElementsByClassName("riddle-cell-value");
        for (var i = 0; i < cellValues.length; i++) {
            var cellValue = cellValues[i].innerHTML;
            if (cellValue.trim() === "") {
                return;
            } else {
                proposal += cellValue;
            }
        }
        RiddleManager.check(proposal, showWinningAnimation);
    }

    function init(pattern, indicators, state, breadth) {
        createIndicators(indicators, breadth);
        createGrid(pattern, state, breadth);
    }

    return {
        init
    };
}());
