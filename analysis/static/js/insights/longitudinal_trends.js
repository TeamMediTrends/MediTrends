document.addEventListener("DOMContentLoaded", function () {
    console.log("Page loaded. Fetching data...");
    fetch("/api/longitudinal-trends/")
        .then(response => response.json())
        .then(data => {
            console.log("Fetched data:", data);
            createChart(data);
        })
        .catch(error => console.error("Error fetching data:", error));
});

function createChart(data) {
    console.log("Chart Data:", data); // Debugging
    const ctx = document.getElementById('longitudinalTrendsChart');
    
    if (!ctx) {
        console.error("Canvas element not found!");
        return;
    }

    const testTypes = Object.keys(data);
    console.log("Test Types:", testTypes);

    const labels = [...new Set(testTypes.flatMap(testType => data[testType].map(entry => entry.date_taken)))];
    console.log("Labels:", labels);

    const datasets = testTypes.map(testType => ({
        label: testType,
        data: labels.map(date => {
            const record = data[testType].find(entry => entry.date_taken === date);
            return record ? record.avg_result : null;
        }),
        borderWidth: 2,
        fill: false,
        tension: 0.3
    }));

    console.log("Datasets:", datasets);

    new Chart(ctx, {
        type: "line",
        data: { labels, datasets },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "top" },
                title: { display: true, text: "Longitudinal Test Trends Over 5 Years" }
            },
            scales: {
                x: { title: { display: true, text: "Date" } },
                y: { title: { display: true, text: "Test Value" } }
            }
        }
    });    
}
