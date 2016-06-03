var RiddleManager;

var Riddle = (function () {

    var select;

    function hidePicker() {
        document.getElementById("picker").classList.add("hide");
    }

    function hideSelectionHighlight() {
        select.classList.remove("selected");
    }

    function endSelection() {
        hidePicker();
        hideSelectionHighlight();
    }

    function showPicker(row, column) {
        var picker = document.getElementById("picker");
        //noinspection JSUnresolvedFunction
        var pickerWidth = picker.getBBox().width;
        //noinspection JSUnresolvedFunction
        var pickerHeight = picker.getBBox().height;

        var svg = document.getElementById("riddle");
        //noinspection JSUnresolvedFunction
        var svgWidth = svg.getBBox().width;
        //noinspection JSUnresolvedFunction
        var svgHeight = svg.getBBox().height;

        var size = RiddleManager.RIDDLE_CELL_SIZE;
        var pickerX = size * (column + 1);
        var pickerY = size * (row + 1);

        if (pickerX + pickerWidth > svgWidth) {
            pickerX = (size * (column - 1)) - pickerWidth;
        }
        if (pickerY + pickerHeight > svgHeight) {
            pickerY = (size * (row - 1)) - pickerHeight;
        }

        var transform = "translate(" + pickerX + ", " + pickerY + ")";
        picker.setAttribute("transform", transform);

        picker.classList.remove("hide");
    }

    function showSelectionHighlight() {
        select.classList.add("selected");
    }

    function startSelection(row, column) {
        showPicker(row, column);
        showSelectionHighlight();
    }

    function createRiddleCellClickFunction(row, column) {
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

    function addRect(parent, x, y, width, height, classNames) {
        var rect = RiddleManager.createSvgElement("rect");
        rect.setAttribute("x", x);
        rect.setAttribute("y", y);
        rect.setAttribute("width", width);
        rect.setAttribute("height", height);

        classNames.forEach(function (className) {
            rect.classList.add(className);
        });

        parent.appendChild(rect);

    }

    function addText(parent, value, x, y, id, classNames) {
        var text = RiddleManager.createSvgElement("text");
        text.setAttribute("id", id);
        text.setAttribute("x", x);
        text.setAttribute("y", y);

        classNames.forEach(function (className) {
            text.classList.add(className);
        });

        var textNode = document.createTextNode(value);
        text.appendChild(textNode);

        parent.appendChild(text);
    }

    function addRiddleCell(pattern, state, row, column, numbers) {
        var values = document.getElementById("riddle-values");

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
        addText(cell, value, textX, textY, id, classNames);

        if (classNames.indexOf("state") !== -1) {
            var riddleCellClickFunction = createRiddleCellClickFunction(row, column);
            cell.addEventListener("click", riddleCellClickFunction);
        }

        values.appendChild(cell);
    }

    function createRiddleCells(pattern, state) {
        var numbers = Math.sqrt(pattern.length);
        for (var row = 0; row < numbers; row++) {
            for (var column = 0; column < numbers; column++) {
                addRiddleCell(pattern, state, row, column, numbers);
            }
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

    function createRiddleGrid(numbers, boxRows, boxColumns) {
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

    function createPickerCellClickFunction(value) {
        return function () {
            var text = select.getElementsByClassName("riddle-cell-value")[0];
            text.innerHTML = value;
            endSelection();
            propose();
        };
    }

    function addPickerCell(value, row, column) {
        var values = document.getElementById("picker-values");

        var cell = RiddleManager.createSvgElement("g");
        cell.classList.add("picker-cell");

        var size = RiddleManager.PICKER_CELL_SIZE;
        var x = size * column;
        var y = size * row;
        var transform = "translate(" + x + ", " + y + ")";
        cell.setAttribute("transform", transform);

        addRect(cell, 0, 0, size, size, ["picker-cell-background"]);

        var textX = size / 2;
        var textY = size / 2;
        var textId = "picker-value-" + value;
        var textClassNames = ["value", "picker-value"];
        addText(cell, value, textX, textY, textId, textClassNames);

        var pickerCellClickFunction = createPickerCellClickFunction(value);
        cell.addEventListener("click", pickerCellClickFunction);

        values.appendChild(cell);
    }

    function calculatePickerSize(numbers) {
        var rows = Math.sqrt(numbers);
        var columns = rows;
        rows = Math.ceil(rows);
        columns = Math.round(columns);
        return {
            rows,
            columns
        };
    }

    function createPickerCells(numbers) {
        var pickerSpecs = calculatePickerSize(numbers);
        var rows = pickerSpecs.rows;
        var columns = pickerSpecs.columns;

        var value = 1;
        for (var row = 0; row < rows; row++) {
            for (var column = 0; column < columns; column++) {
                if (value <= numbers) {
                    addPickerCell(value, row, column);
                }
                value++;
            }
        }
    }

    function createPickerGridRow(columns, size, row, gridOuter, gridInner, borderClassNames) {
        var y = size * row;
        addBorder(gridOuter, 0, y, size, "v", true, borderClassNames);
        addBorder(gridOuter, 0, y, size, "h", true, borderClassNames);
        for (var column = 1; column < columns; column++) {
            var x = size * column;

            var isVBoxBorder = column === 0;
            var isHBoxBorder = row === 0;

            var vGrid = isVBoxBorder ? gridOuter : gridInner;
            var hGrid = isHBoxBorder ? gridOuter : gridInner;

            addBorder(vGrid, x, y, size, "v", isVBoxBorder, borderClassNames);
            addBorder(hGrid, x, y, size, "h", isHBoxBorder, borderClassNames);
        }
        addBorder(gridOuter, size * columns, y, size, "v", true, borderClassNames);
    }

    function createPickerGrid(numbers) {
        var gridInner = document.getElementById("picker-grid-inner");
        var gridOuter = document.getElementById("picker-grid-outer");

        var values = document.getElementById("picker-values");
        // TODO: write Tests for row and column calculation
        var size = RiddleManager.PICKER_CELL_SIZE;
        var pickerSpecs = calculatePickerSize(numbers);
        var rows = pickerSpecs.rows;
        var columns = pickerSpecs.columns;

        var borderClassNames = ["picker-border"];
        for (var row = 0; row < rows; row++) {
            createPickerGridRow(columns, size, row, gridOuter, gridInner, borderClassNames);
        }
        for (var column = 0; column < columns; column++) {
            addBorder(gridOuter, size * column, size * rows, size, "h", true, borderClassNames);
        }

        //noinspection JSUnresolvedFunction
        var bBox = document.getElementById("picker").getBBox();
        var background = document.getElementById("picker-background");
        background.setAttribute("width", bBox.width);
        background.setAttribute("height", bBox.height);
    }

    function init(pattern, state, boxRows) {
        var numbers = Math.sqrt(pattern.length);
        var boxColumns = numbers / boxRows;

        createRiddleCells(pattern, state);
        createRiddleGrid(numbers, boxRows, boxColumns);

        createPickerCells(numbers);
        createPickerGrid(numbers);

        hidePicker();
    }

    return {
        init
    };
}());
