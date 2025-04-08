document.addEventListener("DOMContentLoaded", function () {
    console.log("Population Test Distribution page loaded. Fetching data...");
    fetch("/api/population-test-distribution/")
    .then(response => response.json())
    .then(data => {
        console.log("Fetched distribution data:", data);
        createDistributionCharts(data);
    })
    .catch(error => console.error("Error fetching distribution data:", error));
});

function createDistributionCharts(data) {
    const container = document.getElementById("populationTestDistributionCharts");
    container.innerHTML = ""; // Clear any existing content

    const testTypes = Object.keys(data);
    testTypes.forEach(testType => {
        // Create a wrapper for each chart
        const chartWrapper = document.createElement("div");
        chartWrapper.classList.add("chart-wrapper");

        const title = document.createElement("h3");
        title.textContent = testType;
        chartWrapper.appendChild(title);

        // Create a canvas element for the chart
        const canvas = document.createElement("canvas");
        canvas.id = `chart-${testType.replace(/\s+/g, "-")}`;
        chartWrapper.appendChild(canvas);

        container.appendChild(chartWrapper);

        // Get labels and counts from the data
        const labels = data[testType].labels;
        const counts = data[testType].counts;

        // Create the bar chart using Chart.js
        new Chart(canvas, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Frequency",
                    data: counts,
                    backgroundColor: "rgba(46, 137, 152, 0.6)", // secondary teal with some transparency
                    borderColor: "#004450", // main dark teal
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false // Hide legend if only one dataset
                    },
                    title: {
                        display: true,
                        text: `Distribution of ${testType} Results`,
                        font: {
                            family: 'Poppins',
                            size: 16,
                            weight: 'bold'
                        },
                        color: "#004450"
                    },
                    tooltip: {
                        backgroundColor: "#82dddf",
                        titleColor: "#004450",
                        bodyColor: "#004450"
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Result Range",
                            font: { family: 'Poppins', size: 14, weight: 'bold' },
                            color: "#004450"
                        },
                        ticks: {
                            font: { family: 'Poppins' },
                            color: "#004450"
                        },
                        grid: {
                            color: "#c8c8c8"
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Frequency (# of Tests in Range)",
                            font: { family: 'Poppins', size: 14, weight: 'bold' },
                            color: "#004450"
                        },
                        ticks: {
                            font: { family: 'Poppins' },
                            color: "#004450"
                        },
                        grid: {
                            color: "#c8c8c8"
                        }
                    }
                }
            }
        });
    });
}
