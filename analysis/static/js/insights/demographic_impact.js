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

        document.querySelectorAll(".filter-input").forEach(input => {
            if (input.type === "checkbox" && !input.checked) return;
            if (input.type === "number" && input.value === "") return;

            if (input.type === "number") {
                if (!filters[input.name]) {
                    filters[input.name] = [];
                }
                filters[input.name].push(parseFloat(input.value));
            } else {
                filters[input.name] = input.value;
            }
        });

        fetch(`/api/demographic-impact/?filters=${JSON.stringify(filters)}`)
            .then(response => response.json())
            .then(data => {
                updateCharts(data.test_data);
                criteriaDisplay.textContent = `Selected Criteria: ${JSON.stringify(filters, null, 2)}`;
                percentageDisplay.textContent = `Matching Patients: ${data.selected_percentage}%`;
            });
    }

    function updateCharts(data) {
        resultsContainer.innerHTML = ""; // Clear previous charts

        Object.keys(data).forEach(testName => {
            const canvas = document.createElement("canvas");
            resultsContainer.appendChild(canvas);

            new Chart(canvas, {
                type: "line",
                data: {
                    labels: Object.keys(data[testName]),
                    datasets: [{
                        label: testName,
                        data: Object.values(data[testName]),
                        borderColor: "#004450",
                        backgroundColor: "rgba(0, 68, 80, 0.2)",
                        fill: true,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { title: { display: true, text: "Date" } },
                        y: { title: { display: true, text: "Average Test Value" } }
                    }
                }
            });
        });
    }
});
