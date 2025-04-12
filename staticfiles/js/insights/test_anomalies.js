document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/test-anomalies/")
        .then(response => response.json())
        .then(data => {
             ("Fetched anomalies:", data);
            createHeatmap(data);
            createScatterPlot(data);
            createBoxPlot(data);
            createHistogram(data);
            createAnimatedTimeSeries(data);
            createTable(data);
        })
        .catch(error => console.error("Error fetching anomalies:", error));
});

function createHeatmap(data) {
    // Group anomalies by month (using detected_at date)
    let counts = {};
    data.forEach(item => {
        let date = new Date(item.detected_at);
        let month = date.getFullYear() + "-" + (date.getMonth() + 1);
        counts[month] = (counts[month] || 0) + 1;
    });
    let months = Object.keys(counts).sort();
    let frequencies = months.map(m => counts[m]);

    let trace = {
        z: [frequencies],
        x: months,
        y: ['Anomaly Frequency'],
        type: 'heatmap',
        colorscale: 'Viridis'
    };
    let layout = { title: 'Anomaly Frequency Heatmap (by Month)' };
    Plotly.newPlot('heatmap', [trace], layout);
}

function createScatterPlot(data) {
    // Plot anomaly deviation scores over time
    let x = data.map(item => new Date(item.detected_at));
    let y = data.map(item => item.deviation_score);
    let text = data.map(item => item.test_type + " (Patient " + item.patient_id + ")");

    let trace = {
        x: x,
        y: y,
        mode: 'markers',
        type: 'scatter',
        text: text,
        marker: { size: 8, color: 'red' }
    };
    let layout = {
        title: 'Scatter Plot of Anomalies (Deviation Score vs. Time)',
        xaxis: { title: 'Detected At' },
        yaxis: { title: 'Deviation Score' }
    };
    Plotly.newPlot('scatter', [trace], layout);
}

function createBoxPlot(data) {
    // Box plot per test type: group anomalies by test_type
    let groups = {};
    data.forEach(item => {
        if (!groups[item.test_type]) groups[item.test_type] = [];
        groups[item.test_type].push(item.test_value);
    });
    let traces = [];
    for (let test in groups) {
        traces.push({
            y: groups[test],
            type: 'box',
            name: test
        });
    }
    let layout = { title: 'Box Plot of Anomalous Test Values by Test Type' };
    Plotly.newPlot('boxplot', traces, layout);
}

function createHistogram(data) {
    // Histogram of anomalous test values
    let values = data.map(item => item.test_value);
    let trace = {
        x: values,
        type: 'histogram',
        marker: { color: 'blue' }
    };
    let layout = {
        title: 'Histogram of Anomalous Test Values',
        xaxis: { title: 'Test Value' },
        yaxis: { title: 'Frequency' }
    };
    Plotly.newPlot('histogram', [trace], layout);
}

function createAnimatedTimeSeries(data) {
    // For each month, calculate the average deviation score.
    let grouped = {};
    data.forEach(item => {
        let date = new Date(item.detected_at);
        let month = date.getFullYear() + "-" + (date.getMonth() + 1);
        if (!grouped[month]) grouped[month] = [];
        grouped[month].push(item.deviation_score);
    });
    let months = Object.keys(grouped).sort();
    let avgScores = months.map(month => {
        let scores = grouped[month];
        return scores.reduce((sum, s) => sum + s, 0) / scores.length;
    });

    let trace = {
        x: months,
        y: avgScores,
        mode: 'lines+markers',
        type: 'scatter'
    };

    let layout = {
        title: 'Animated Time-Series of Average Deviation Score by Month',
        xaxis: { title: 'Month' },
        yaxis: { title: 'Average Deviation Score' },
        updatemenus: [{
            type: "buttons",
            showactive: false,
            buttons: [{
                label: "Play",
                method: "animate",
                args: [null, { frame: { duration: 500, redraw: true }, transition: { duration: 300 }, fromcurrent: true }]
            }]
        }]
    };

    // Create frames for animation
    let frames = months.map((month, i) => ({
        name: month,
        data: [{
            x: months.slice(0, i + 1),
            y: avgScores.slice(0, i + 1)
        }]
    }));

    Plotly.newPlot('animated-timeseries', [trace], layout).then(function () {
        Plotly.addFrames('animated-timeseries', frames);
    });
}

function createTable(data) {
    // Build an HTML table for anomaly details
    let tableDiv = document.getElementById("anomalies-table");
    let html = "<table border='1' style='width:100%; margin-top:20px;'><thead><tr>" +
        "<th>Patient ID</th><th>Test Type</th><th>Test Value</th>" +
        "<th>Deviation Score</th><th>Detected At</th></tr></thead><tbody>";
    data.forEach(item => {
        html += `<tr>
        <td>${item.patient_id}</td>
        <td>${item.test_type}</td>
        <td>${item.test_value}</td>
        <td>${item.deviation_score}</td>
        <td>${new Date(item.detected_at).toLocaleString()}</td>
        </tr>`;
    });
    html += "</tbody></table>";
    tableDiv.innerHTML = html;
}
