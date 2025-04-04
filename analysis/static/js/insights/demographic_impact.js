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

        // Iterate over all filter inputs
        document.querySelectorAll(".filter-input").forEach(input => {
            if (!input.name) return; // Ensure input has a name

            if (input.type === "checkbox") {
                if (input.checked) {
                    filters[input.name] = true; // If checked, set value to true
                }
            } else if (input.type === "number" && input.value !== "") {
                filters[input.name] = input.value;
            } else if (input.tagName === "SELECT" && input.name === "state") {
                // Handle multi-select for state
                const selectedStates = Array.from(input.selectedOptions)
                    .map(option => option.value);
                if (selectedStates.length > 0) {
                    filters.state = selectedStates; // Store selected states as an array
                }
            } else if (input.tagName === "SELECT" && input.name === "sex") {
                const selectedSex = Array.from(input.selectedOptions)
                    .map(option => option.value);
                if (selectedSex.length > 0) {
                    filters.sex = selectedSex;
                }
            } else if (input.tagName === "SELECT" && input.name === "marital_status") {
                const selectedMaritalStatus = Array.from(input.selectedOptions)
                    .map(option => option.value);
                if (selectedMaritalStatus.length > 0) {
                    filters.marital_status = selectedMaritalStatus; // Store selected value
                }
            } else if (input.tagName === "SELECT" && input.name === "education_level") {
                const selectedEducationLevel = Array.from(input.selectedOptions)
                    .map(option => option.value);
                if (selectedEducationLevel.length > 0) {
                    filters.education_level = selectedEducationLevel; // Store selected value
                }
            } else if (input.tagName === "SELECT" && input.name === "ethnicity") {
                const selectedEthnicity = Array.from(input.selectedOptions)
                    .map(option => option.value);
                if (selectedEthnicity.length > 0) {
                    filters.ethnicity = selectedEthnicity; // Store selected value
                }
            } else if (input.tagName === "SELECT" && input.name === "insurance_status") {
                const selectedInsuranceStatus = Array.from(input.selectedOptions)
                    .map(option => option.value);
                if (selectedInsuranceStatus.length > 0) {
                    filters.insurance_status = selectedInsuranceStatus; // Store selected value
                }
            } else if (input.tagName === "SELECT" && input.name === "dependents") {
                const selectedDependents = Array.from(input.selectedOptions)
                    .map(option => option.value);
                if (selectedDependents.length > 0) {
                    filters.dependents = selectedDependents; // Store selected value
                }
            } else if (input.tagName === "SELECT" && input.name === "income") {
                const selectedIncome = Array.from(input.selectedOptions)
                    .map(option => option.value);
                if (selectedIncome.length > 0) {
                    filters.income = selectedIncome;
                }
            } else if (input.tagName === "INPUT" && input.name === "min_age") {
                if (input.value !== "") {
                    filters[input.name] = input.value;
                }
            } else if (input.tagName === "INPUT" && (input.name === "max_age")) {
                if (input.value !== "") {
                    filters[input.name] = input.value;
                }
            } else if (input.value) {
                // Handle other types of inputs like text fields, etc.
                filters[input.name] = input.value;
            }
        });

        if (Object.keys(filters).length === 0) {
            console.warn("No valid filters selected.");
            return;
        }

        console.log("Filters being sent:", filters);

        // Encode the filters object and send it to the API
        const apiUrl = `/api/demographic-impact/?filters=${encodeURIComponent(JSON.stringify(filters))}`;
        console.log("API Request URL:", apiUrl);

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                console.log("API Response:", data);
                updateCharts(data.test_data);
                criteriaDisplay.textContent = `Selected Criteria: ${JSON.stringify(filters, null, 2)}`;
                percentageDisplay.textContent = `Matching Patients: ${data.selected_percentage}%`;
            })
            .catch(error => console.error("Error fetching data:", error));
    }

    // function updateCharts(data) {
    //     resultsContainer.innerHTML = ""; // Clear previous charts

    //     Object.keys(data).forEach(testName => {
    //         const canvas = document.createElement("canvas");
    //         resultsContainer.appendChild(canvas);

    //         new Chart(canvas, {
    //             type: "line",
    //             data: {
    //                 labels: Object.keys(data[testName]),
    //                 datasets: [{
    //                     label: testName,
    //                     data: Object.values(data[testName]),
    //                     borderColor: "#004450",
    //                     backgroundColor: "rgba(0, 68, 80, 0.2)",
    //                     fill: true,
    //                 }]
    //             },
    //             options: {
    //                 responsive: true,
    //                 maintainAspectRatio: false,
    //                 scales: {
    //                     x: { title: { display: true, text: "Date" } },
    //                     y: { title: { display: true, text: "Average Test Value" } }
    //                 }
    //             }
    //         });
    //     });
    // }
});
