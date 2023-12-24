var selectedRobotForChart = "";

function createRobotSelection() {
    robotSelection = document.createElement("select");
    robotSelection.id = "closestRobotName";
    var previousRobotNameSelection = document.getElementById("closestRobotName");
    if (previousRobotNameSelection != null) {
        previousRobotNameSelection.parentNode.removeChild(previousRobotNameSelection);
    }
    return robotSelection;
}

function createOption(value, disabled, selected, text, parent) {
    var option = document.createElement("option");
    option.value = value;
    option.disabled = disabled;
    option.selected = selected;
    option.text = text;
    parent.appendChild(option);
}

function createAndPopulateSelect(data) {
    var select = createRobotSelection();
    createOption("", true, true, "Select robot model", select);
    for (var i = 0; i < data.length; i++) {
        createOption(data[i].label, false, false, data[i].label + " - Reach(mm) " +
            data[i].data[0].x + " - Payload(kg) " + data[i].data[0].y, select);
    }
    return select;
}

function setupChangeListener(select) {
    select.addEventListener("change", () => {
        robotSelectionChanged(select);
        selectedRobotForChart = select.value;
        highlightOnChart(selectedRobotForChart);
    });
}

function getDataWithDistance(data, reach, payload) {
    var dataWithDistance = data;
    for (var i = 0; i < dataWithDistance.length; i++) {
        var distance = Math.sqrt(Math.pow(dataWithDistance[i].data[0].x - reach, 2) / 10 + Math.pow(dataWithDistance[i].data[0].y - payload, 2));
        dataWithDistance[i].distance = distance;
    }
    return dataWithDistance;
}

function getDataOnlyBiggestSrongest(data, reach, payload) {
    var dataOnlyBiggestSrongest = data.filter(function (element) {
        return element.data[0].x >= reach && element.data[0].y >= payload;
    });
    dataOnlyBiggestSrongest = sortDataBy(dataOnlyBiggestSrongest, "distance");
    return dataOnlyBiggestSrongest;
}

function completeDatatable(datatable, data, size) {
    while (datatable.length != size && data.length != 0) {
        var firstElement = data.shift();
        var isAlreadyIncluded = datatable.some(function (element) {
            return element === firstElement;
        });
        if (!isAlreadyIncluded) {
            datatable.push(firstElement);
        }
    }
    return datatable;
}

function getClosestRobots(brand, reach, payload) {
    var brands = getBrands();
    var closestRobots = [];
    for (var i = 0; i < brands.length; i++) {
        var other_brand = brands[i];
        if (other_brand != brand && other_brand != "") {
            var data = getDatasets(other_brand);
            data = getDataWithDistance(data, reach, payload);
            data = sortDataBy(data, "distance");
            datasorted = getDataOnlyBiggestSrongest(data, reach, payload);
            datatable = []
            // try to add the 2 robots with biggest reach and payload
            if (datasorted[0] != null) {
                datatable.push(datasorted[0])
            }
            if (datasorted[1] != null) {
                datatable.push(datasorted[1])
            }
            // complete with the closest robots
            datatable = completeDatatable(datatable, data, 3);
            for (var k = 0; k < datatable.length; k++) {
                datatable[k].brand = other_brand;
                closestRobots.push(datatable[k]);
            }
        }
    }
    return closestRobots;
}

function getBrands() {
    var options = closestRobotBrandSelection.options;
    var brands = [];
    for (var i = 0; i < options.length; i++) {
        brands.push(options[i].value);
    }
    return brands;
}

function deletePreviousClosestRobots() {
    var previousClosestRobots = document.getElementById("closestRobots");
    if (previousClosestRobots != null) {
        previousClosestRobots.parentNode.removeChild(previousClosestRobots);
    }
}

function createTable(id) {
    var table = document.createElement("table");
    table.id = id;
    return table;
}

function createHeaderRow(table) {
    var headerRow = document.createElement("tr");
    ["Brand", "Name", "Reach (mm)", "Payload (kg)"].forEach(text => {
        var th = document.createElement("th");
        th.innerHTML = text;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);
}

function createTableCell(text, className, cellHeight = 1) {
    var td = document.createElement("td");
    td.innerHTML = text;
    td.rowSpan = cellHeight;
    if (className) {
        td.classList.add(className);
    }
    return td;
}

function populateTable(table, closestRobots) {
    var firstRobotFromBrand = true;
    var brand = "";
    closestRobots.forEach(robot => {
        var row = document.createElement("tr");
        if (brand != robot.brand) {
            brand = robot.brand;
            firstRobotFromBrand = true;
        }
        if (firstRobotFromBrand) {
            row.appendChild(createTableCell(robot.brand, "brand", 3));
            firstRobotFromBrand = false;
        }
        row.appendChild(createTableCell(robot.label));
        row.appendChild(createTableCell(robot.data[0].x, "reach"));
        row.appendChild(createTableCell(robot.data[0].y, "payload"));
        table.appendChild(row);
    });
}


function displayClosestRobotsTable(closestRobots) {
    deletePreviousClosestRobots();
    var table = createTable("closestRobots");
    createHeaderRow(table);
    populateTable(table, closestRobots);
    var closestRobotSelection = document.getElementById("closestRobotSelection");
    closestRobotSelection.appendChild(table);
}

function robotSelectionChanged(selectedRobot) {
    var brand = closestRobotBrandSelection.value;
    var dataset = getDatasets(brand);
    var name = selectedRobot.value;
    var robot = dataset.find(function (element) {
        return element.label == name;
    });
    var reach = robot.data[0].x;
    var payload = robot.data[0].y;
    displayClosestRobotsTable(getClosestRobots(brand, reach, payload));
}

function brandSelectionChanged() {
    var brand = this.value;
    var data = getDatasets(brand);
    data = sortDataBy(data, "payload");
    var select = createAndPopulateSelect(data);
    this.parentNode.insertBefore(select, this.nextSibling);
    setupChangeListener(select);
}

var closestRobotBrandSelection = document.getElementById("closestRobotBrand");
closestRobotBrandSelection.addEventListener("change", brandSelectionChanged);


