function getDatasets(brand) {
    var datasets = [];
    if (brand != "ABB") {
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                var robot = data[key];
                if (robot.MT == "R" && robot.T == "6 DOF") {
                    if (robot.B == brand) {
                        datasets.push({
                            label: getLabelFromName(robot.N),
                            data: [{
                                x: robot.R,
                                y: robot.P
                            }],
                            backgroundColor: robotColor(robot.B),
                            pointRadius: 3
                        });
                    }
                }
            }
        }
    } else {
        abb_library = myJson.items;
        for (var i = 0; i < abb_library.length; i++) {
            if ((abb_library[i].product_type == "Articulated") && !["IRB 460", "IRB 760", "IRB 660"].includes(abb_library[i].product_name)) {
                for (var j = 0; j < abb_library[i].variants.length; j++) {
                    var robot = abb_library[i].variants[j];
                    datasets.push({
                        label: robot.name,
                        data: [{
                            x: robot.reach * 1000,
                            y: robot.capacity
                        }],
                        backgroundColor: robotColor("ABB"),
                        pointRadius: 3,
                        pointBorderColor: "rgba(0,0,0,0.5)"
                    });

                }
            }
        }
    }
    return datasets;
}

function sortDataByReach(data, decreasing = false) {
    data.sort(function (a, b) {
        if (decreasing) {
            return b.data[0].x - a.data[0].x;
        } else {
            return a.data[0].x - b.data[0].x;
        }
    });
    return data;
}

function sortDataByPayload(data, decreasing = false) {
    data.sort(function (a, b) {
        if (decreasing) {
            return b.data[0].y - a.data[0].y;
        } else {
            return a.data[0].y - b.data[0].y;
        }
    });
    return data;
}

function sortDataByDistance(data, decreasing = false) {
    data.sort(function (a, b) {
        if (decreasing) {
            return b.distance - a.distance;
        } else {
            return a.distance - b.distance;
        }
    });
    return data;
}

function sortDataBy(data, criteria, decreasing = false) {
    if (criteria == "reach") {
        return sortDataByReach(data, decreasing);
    } else if (criteria == "payload") {
        return sortDataByPayload(data, decreasing);
    } else if (criteria == "distance") {
        return sortDataByDistance(data, decreasing);
    }
}

function getLabelFromName(name) {
    var label = name.replace(/(Fanuc|KUKA|Staubli|Yaskawa Motoman|Yaskawa|Motoman|ABB)/g, "").trim();
    return label;
}