import * as RiddleManager from './riddle-manager.js';

let select;

function hidePicker() {
    document.getElementById("picker").classList.add("picker-hidden");
}

function hideSelectionHighlight() {
    select.classList.remove("selected");
}

function endSelection() {
    hidePicker();
    hideSelectionHighlight();
}

function showPicker(row, column) {
    const picker = document.getElementById("picker");
    //noinspection JSUnresolvedFunction
    const pickerWidth = picker.getBBox().width;
    //noinspection JSUnresolvedFunction
    const pickerHeight = picker.getBBox().height;

    const svg = document.getElementById("riddle");
    //noinspection JSUnresolvedFunction
    const svgWidth = svg.getBBox().width;
    //noinspection JSUnresolvedFunction
    const svgHeight = svg.getBBox().height;

    const size = RiddleManager.RIDDLE_CELL_SIZE;
    let pickerX = size * (column + 1);
    let pickerY = size * (row + 1);

    if (pickerX + pickerWidth > svgWidth) {
        pickerX = (size * (column - 1)) - pickerWidth;
    }
    if (pickerY + pickerHeight > svgHeight) {
        pickerY = (size * (row - 1)) - pickerHeight;
    }

    const transform = "translate(" + pickerX + ", " + pickerY + ")";
    picker.setAttribute("transform", transform);

    picker.classList.remove("picker-hidden");
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
        const picker = document.getElementById("picker");
        const pickerIsOpen = !picker.classList.contains("picker-hidden");

        if (select) {
            endSelection();
        }
        const isClosing = select === this && pickerIsOpen;
        if (!isClosing) {
            select = this;
            startSelection(row, column);
        }
    };
}

function addRect(parent, x, y, width, height, classNames) {
    const rect = RiddleManager.createSvgElement("rect");
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
    const text = RiddleManager.createSvgElement("text");
    text.setAttribute("id", id);
    text.setAttribute("x", x);
    text.setAttribute("y", y);

    classNames.forEach(function (className) {
        text.classList.add(className);
    });

    const textNode = document.createTextNode(value);
    text.appendChild(textNode);

    parent.appendChild(text);
}

function addRiddleCell(pattern, state, row, column, numbers) {
    const values = document.getElementById("riddle-values");

    const cell = RiddleManager.createSvgElement("g");
    cell.classList.add("riddle-cell");

    const size = RiddleManager.RIDDLE_CELL_SIZE;
    const x = size * column;
    const y = size * row;
    const transform = "translate(" + x + ", " + y + ")";
    cell.setAttribute("transform", transform);

    const classNames = ["value", "riddle-cell-value"];

    let value = pattern[row * numbers + column];
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

    const textX = size / 2;
    const textY = size / 2;
    const id = "riddle-value-" + row + "-" + column;
    addText(cell, value, textX, textY, id, classNames);

    if (classNames.indexOf("state") !== -1) {
        const riddleCellClickFunction = createRiddleCellClickFunction(row, column);
        cell.addEventListener("click", riddleCellClickFunction);
    }

    values.appendChild(cell);
}

function createRiddleCells(pattern, state) {
    const numbers = Math.sqrt(pattern.length);
    for (let row = 0; row < numbers; row++) {
        for (let column = 0; column < numbers; column++) {
            addRiddleCell(pattern, state, row, column, numbers);
        }
    }
}

function addBorder(parent, x, y, size, orientation, isBold, classNames) {
    const border = RiddleManager.createSvgElement("line");
    border.setAttribute("stroke-linecap", "square");

    border.classList.add("border");
    classNames.forEach(function (className) {
        border.classList.add(className);
    });
    if (isBold) {
        border.classList.add("bold");
    }

    let x2 = x;
    let y2 = y;
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
    const y = size * row;
    for (let column = 0; column < numbers; column++) {
        const x = size * column;

        const isVBoxBorder = column % boxColumns === 0;
        const isHBoxBorder = row % boxRows === 0;

        const vGrid = isVBoxBorder ? gridBold : gridThin;
        const hGrid = isHBoxBorder ? gridBold : gridThin;

        addBorder(vGrid, x, y, size, "v", isVBoxBorder, classNames);
        addBorder(hGrid, x, y, size, "h", isHBoxBorder, classNames);
    }
    // create rightmost vertical border
    addBorder(gridBold, size * numbers, y, size, "v", true, classNames);
}

function createRiddleGrid(numbers, boxRows, boxColumns) {
    const gridThin = document.getElementById("riddle-grid-thin");
    const gridBold = document.getElementById("riddle-grid-bold");

    const size = RiddleManager.RIDDLE_CELL_SIZE;
    const classNames = [];

    for (let row = 0; row < numbers; row++) {
        createRiddleGridRow(numbers, size, row, boxColumns, boxRows, gridBold, gridThin, classNames);
    }
    // create lowest horizontal borders
    for (let column = 0; column < numbers; column++) {
        const lastRowBorderX = size * column;
        const lastRowBorderY = size * numbers;
        addBorder(gridBold, lastRowBorderX, lastRowBorderY, size, "h", true, classNames);
    }
}

function showWinningAnimation() {
    const backgrounds = document.getElementsByClassName("riddle-cell-background");
    for (let i = 0; i < backgrounds.length; i++) {
        backgrounds[i].classList.add("winning");
    }
}

function propose() {
    let proposal = "";
    const cellValues = document.getElementsByClassName("riddle-cell-value");
    for (let i = 0; i < cellValues.length; i++) {
        const cellValue = cellValues[i].innerHTML;
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
        const text = select.getElementsByClassName("riddle-cell-value")[0];
        text.innerHTML = value;
        endSelection();
        propose();
    };
}

function addPickerCell(value, row, column) {
    const values = document.getElementById("picker-values");

    const cell = RiddleManager.createSvgElement("g");
    cell.classList.add("picker-cell");

    const size = RiddleManager.PICKER_CELL_SIZE;
    const x = size * column;
    const y = size * row;
    const transform = "translate(" + x + ", " + y + ")";
    cell.setAttribute("transform", transform);

    addRect(cell, 0, 0, size, size, ["picker-cell-background"]);

    const textX = size / 2;
    const textY = size / 2;
    const textId = "picker-value-" + value;
    const textClassNames = ["value", "picker-value"];
    addText(cell, value, textX, textY, textId, textClassNames);

    const pickerCellClickFunction = createPickerCellClickFunction(value);
    cell.addEventListener("click", pickerCellClickFunction);

    values.appendChild(cell);
}

function calculatePickerSize(numbers) {
    let rows = Math.sqrt(numbers);
    let columns = rows;
    rows = Math.ceil(rows);
    columns = Math.round(columns);
    return {
        rows,
        columns
    };
}

function createPickerCells(numbers) {
    const pickerSpecs = calculatePickerSize(numbers);
    const rows = pickerSpecs.rows;
    const columns = pickerSpecs.columns;

    let value = 1;
    for (let row = 0; row < rows; row++) {
        for (let column = 0; column < columns; column++) {
            if (value <= numbers) {
                addPickerCell(value, row, column);
            }
            value++;
        }
    }
}

function createPickerGridRow(columns, size, row, gridOuter, gridInner, borderClassNames) {
    const y = size * row;
    for (let column = 0; column < columns; column++) {
        const x = size * column;

        const isVBoxBorder = column === 0;
        const isHBoxBorder = row === 0;

        const vGrid = isVBoxBorder ? gridOuter : gridInner;
        const hGrid = isHBoxBorder ? gridOuter : gridInner;

        addBorder(vGrid, x, y, size, "v", isVBoxBorder, borderClassNames);
        addBorder(hGrid, x, y, size, "h", isHBoxBorder, borderClassNames);
    }
    addBorder(gridOuter, size * columns, y, size, "v", true, borderClassNames);
}

function createPickerGrid(numbers) {
    const gridInner = document.getElementById("picker-grid-inner");
    const gridOuter = document.getElementById("picker-grid-outer");

    const values = document.getElementById("picker-values");
    // TODO: write Tests for row and column calculation
    const size = RiddleManager.PICKER_CELL_SIZE;
    const pickerSpecs = calculatePickerSize(numbers);
    const rows = pickerSpecs.rows;
    const columns = pickerSpecs.columns;

    const borderClassNames = ["picker-border"];
    for (let row = 0; row < rows; row++) {
        createPickerGridRow(columns, size, row, gridOuter, gridInner, borderClassNames);
    }
    for (let column = 0; column < columns; column++) {
        addBorder(gridOuter, size * column, size * rows, size, "h", true, borderClassNames);
    }

    //noinspection JSUnresolvedFunction
    const bBox = document.getElementById("picker").getBBox();
    const background = document.getElementById("picker-background");
    background.setAttribute("width", bBox.width);
    background.setAttribute("height", bBox.height);
}

export function init(pattern, state, boxRows = Math.pow(pattern.length, 1 / 4)) {
    const numbers = Math.sqrt(pattern.length);
    const boxColumns = numbers / boxRows;

    createRiddleCells(pattern, state);
    createRiddleGrid(numbers, boxRows, boxColumns);

    createPickerCells(numbers);
    createPickerGrid(numbers);

    hidePicker();
}
