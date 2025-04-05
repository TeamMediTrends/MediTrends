document.addEventListener("DOMContentLoaded", function () {
    const filterForm = document.getElementById("demographic-filter-form");
    const resultsContainer = document.getElementById("results-container");
    const criteriaDisplay = document.getElementById("selected-criteria");
    const percentageDisplay = document.getElementById("selected-percentage");

    filterForm.addEventListener("submit", function (event) {
        event.preventDefault();
        fetchFilteredData();
    });

    function fetchFilteredData() {
        const filters = {};

        document.querySelectorAll(".filter-input").forEach((input) => {
            const name = input.name;
            if (!name) return;

            const tag = input.tagName;
            const type = input.type;

            // Checkbox
            if (type === "checkbox") {
                if (input.checked) {
                    filters[name] = true;
                }
                return;
            }

            // Number and text inputs
            if ((type === "number" || type === "text") && input.value !== "") {
                filters[name] = input.value;
                return;
            }

            // Select inputs (including multi-selects)
            if (tag === "SELECT") {
                const selected = Array.from(input.selectedOptions)
                    .map((opt) => opt.value)
                    .filter((v) => v !== "");
                if (selected.length > 0) {
                    filters[name] = selected;
                }
                return;
            }

            // Other inputs
            if (input.value) {
                filters[name] = input.value;
            }
        });

        if (Object.keys(filters).length === 0) {
            console.warn("No valid filters selected.");
            return;
        }

        console.log("Filters being sent:", filters);

        const apiUrl = `/api/demographic-impact/?filters=${encodeURIComponent(
            JSON.stringify(filters)
        )}`;
        console.log("API Request URL:", apiUrl);

        // Show loading icon
        const loadingIcon = document.getElementById("loading-icon");
        loadingIcon.style.display = "block";  // Show loading icon
        resultsContainer.innerHTML = ""; // Clear previous results

        fetch(apiUrl)
            .then((response) => response.json())
            .then((data) => {
                console.log("API Response:", data);

                // Update chart with test_data
                createCharts(data);

                // Display matched group percentage
                percentageDisplay.textContent = `Percentage of Patients That Match Filters: ${data.patient_percentage.toFixed(
                    2
                )}%`; // Use data.patient_percentage and limit to two decimal places

                // Hide loading icon after data is successfully fetched
                loadingIcon.style.display = "none";  // Hide loading icon
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                resultsContainer.innerHTML =
                    "<p>Error fetching data. Please try again later.</p>";

                // Hide loading icon in case of error
                loadingIcon.style.display = "none";  // Hide loading icon
            });
    }
});

function createCharts(data) {
    const container = document.getElementById("results-container");
    container.innerHTML = ""; // Clear previous charts

    const groupedByTest = {};

    data.test_data.forEach((entry) => {
        if (!groupedByTest[entry.test_type]) {
            groupedByTest[entry.test_type] = [];
        }
        groupedByTest[entry.test_type].push(entry);
    });

    const testTypes = Object.keys(groupedByTest);
    console.log("Test Types:", testTypes);

    testTypes.forEach((testType) => {
        const chartDiv = document.createElement("div");
        chartDiv.classList.add("chart-wrapper");

        // Assuming the test_type key holds the test name now
        const title = document.createElement("h3");
        title.textContent = testType; // This is now the test name

        const canvas = document.createElement("canvas");
        canvas.id = `chart-${testType.replace(/\s+/g, "-")}`;

        chartDiv.appendChild(title);
        chartDiv.appendChild(canvas);
        container.appendChild(chartDiv);

        const labels = [
            ...new Set(
                groupedByTest[testType].map((entry) => entry.date_taken)
            ),
        ];

        const dataset = {
            label: testType,
            data: labels.map((date) => {
                const record = groupedByTest[testType].find(
                    (entry) => entry.date_taken === date
                );
                return record ? record.result : null;
            }),
            borderWidth: 2,
            fill: false,
            tension: 0.3,
        };

        new Chart(canvas, {
            type: "line",
            data: {
                labels: labels,
                datasets: [dataset],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                    },
                    title: {
                        display: false,
                    },
                },
            },
        });
    });
}
