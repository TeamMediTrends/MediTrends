document.addEventListener("DOMContentLoaded", function () {
     ("Page loaded. Fetching test data...");

    // Fetch the test data from the API
    fetch("/api/patient-test-levels/")
        .then((response) => response.json())
        .then((data) => {
            if (data.test_data) {
                createTestScatterPlots(data.test_data); // data.test_data should be an array
            } else {
                console.error("Error: No test data in the response.");
            }
        })
        .catch((error) => {
            console.error("Error fetching test data:", error);
        });
});

function createTestScatterPlots(testData) {
     ("Test Data:", testData); // Debugging

    const container = document.getElementById("test-chart");
    container.innerHTML = ""; // Clear previous charts if any

    testData.forEach((test) => {
        // Create a new div and canvas for each test
        const chartDiv = document.createElement("div");
        chartDiv.classList.add("chart-wrapper");

        // Add test name as the title
        const title = document.createElement("h3");
        title.textContent = test.test_name;

        const canvas = document.createElement("canvas");
        canvas.id = `chart-${test.test_name.replace(/\s+/g, "-")}`; // Unique ID for each chart

        chartDiv.appendChild(title);
        chartDiv.appendChild(canvas);
        container.appendChild(chartDiv);

        // Create labels (patient IDs or custom labels based on data structure)
        const labels = Array.from({ length: test.levels.length }, (_, i) => `Patient ${i + 1}`);

        // Create dataset for this test (scatter plot)
        const dataset = {
            label: test.test_name,
            data: test.levels.map((level, index) => ({
                x: index + 1,  // Use patient index for x-axis
                y: level,      // Test level for y-axis
            })),
            backgroundColor: "#2e8998",
            borderColor: "#2e8998",
            borderWidth: 1,
            pointRadius: 3,
        };

        // Draw chart
        new Chart(canvas, {
            type: "scatter",
            data: {
                labels, 
                datasets: [dataset],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { 
                        display: false,  // Hide the legend
                    },
                    tooltip: {
                        callbacks: {
                            label: function (tooltipItem) {
                                return `Level: ${tooltipItem.raw.y}`;
                            },
                        },
                    },
                    title: {
                        display: true,
                        text: `Test Data for ${test.test_name}`,
                        font: {
                            family: "Poppins",
                            size: 18,
                            weight: "bold",
                        },
                        color: "#004450",
                    },
                },
                scales: {
                    x: {
                        title: {
                            display: false, 
                        },
                        ticks: {
                            display: false,
                        },
                        grid: {
                            color: "#c8c8c8",
                        },
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Test Level",
                            font: {
                                family: "Poppins",
                                size: 14,
                                weight: "bold",
                            },
                            color: "#004450",
                        },
                        ticks: {
                            font: {
                                family: "Poppins",
                            },
                            color: "#004450",
                        },
                        grid: {
                            color: "#c8c8c8",
                        },
                    },
                },
            },
        });
    });
}
