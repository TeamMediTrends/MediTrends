document.addEventListener("DOMContentLoaded", function () {
    console.log("Page loaded. Fetching data...");
    fetch("/api/longitudinal-trends/")
        .then(response => response.json())
        .then(data => {
            console.log("Fetched data:", data);
            createCharts(data);
        })
        .catch(error => console.error("Error fetching data:", error));
});

function createCharts(data) {
    console.log("Chart Data:", data); // Debugging

    const container = document.getElementById("longitudinalTrendsCharts");
    container.innerHTML = ""; // Clear previous charts if any

    const testTypes = Object.keys(data);
    console.log("Test Types:", testTypes);

    testTypes.forEach(testType => {
        // Create a new div and canvas for each test type
        const chartDiv = document.createElement("div");
        chartDiv.classList.add("chart-wrapper");

        const title = document.createElement("h3");
        title.textContent = testType;

        const canvas = document.createElement("canvas");
        canvas.id = `chart-${testType.replace(/\s+/g, "-")}`; // Unique ID

        chartDiv.appendChild(title);
        chartDiv.appendChild(canvas);
        container.appendChild(chartDiv);

        // Extract labels (dates)
        const labels = [...new Set(data[testType].map(entry => entry.date_bucket))];

        // Extract dataset for this test type
        const dataset = {
            label: testType,
            data: labels.map(date => {
                const record = data[testType].find(entry => entry.date_bucket === date);
                return record ? record.avg_result : null;
            }),
            borderWidth: 2,
            fill: false,
            tension: 0.3
        };

        // Draw chart
        new Chart(canvas, {
            type: "line",
            data: { labels, datasets: [dataset] },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "top" },
                    title: { display: true, text: `Trends for ${testType}` }
                },
                scales: {
                    x: { title: { display: true, text: "Date" } },
                    y: { title: { display: true, text: "Test Value" } }
                }
            }
        });
    });
}
