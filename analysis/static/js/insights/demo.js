document.addEventListener("DOMContentLoaded", function () {
    const filterForm = document.getElementById("filter-form");
    const resultsContainer = document.getElementById("results-container");

    filterForm.addEventListener("submit", function (event) {
        event.preventDefault();
        fetchFilteredData();
    });

    function fetchFilteredData() {
        const filters = {};

        // Get selected filter values
        const sexFilter = document.getElementById("sex-select").value;
        filters.sex = sexFilter;

        const apiUrl = `/api/demo-filter-results/?filters=${encodeURIComponent(JSON.stringify(filters))}`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultsContainer.innerHTML = `<p>Error: ${data.error}</p>`;
                } else {
                    displayResults(data);
                }
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                resultsContainer.innerHTML = `<p>Error fetching data from server.</p>`;
            });
    }

    function displayResults(data) {
        resultsContainer.innerHTML = "<h3>Filtered Test Results:</h3>";
        const resultList = document.createElement("ul");
        data.test_data.forEach(result => {
            const listItem = document.createElement("li");
            listItem.textContent = `Test Name: ${result.test_type}, Date Taken: ${result.date_taken}, Result: ${result.result}`;
            resultList.appendChild(listItem);
        });
        resultsContainer.appendChild(resultList);
    }
});
