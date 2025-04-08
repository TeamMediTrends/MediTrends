document.addEventListener("DOMContentLoaded", function () {
    console.log("Correlation Analysis page loaded. Fetching data...");
    fetch("/api/test-correlation/")
        .then(response => response.json())
        .then(data => {
            console.log("Fetched correlation data:", data);
            createCorrelationTable(data);
        })
        .catch(error => console.error("Error fetching correlation data:", error));
});

function createCorrelationTable(data) {
    const container = document.getElementById("testCorrelationContainer");
    container.innerHTML = "";  // Clear previous content

    // Extract test types (i.e., column names in the correlation matrix)
    const testTypes = Object.keys(data);

    // Create a table element
    const table = document.createElement("table");
    table.classList.add("correlation-table");

    // Create header row
    const headerRow = document.createElement("tr");
    const emptyCell = document.createElement("th");
    headerRow.appendChild(emptyCell); // top-left empty cell
    testTypes.forEach(test => {
        const th = document.createElement("th");
        th.textContent = test;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    // Create table rows for each test type
    testTypes.forEach(rowTest => {
        const row = document.createElement("tr");
        const rowHeader = document.createElement("th");
        rowHeader.textContent = rowTest;
        row.appendChild(rowHeader);

        testTypes.forEach(colTest => {
            const cell = document.createElement("td");
            const value = data[rowTest][colTest];
            // Format the correlation value to two decimals
            const formatted = (value !== undefined ? value.toFixed(2) : "N/A");
            cell.textContent = formatted;
            // Color-code the cell based on correlation strength and sign
            if (value >= 0) {
                // Positive correlation: shades of green
                const intensity = Math.min(255, Math.floor(255 - value * 100));
                cell.style.backgroundColor = `rgb(${intensity}, 255, ${intensity})`;
            } else {
                // Negative correlation: shades of red
                const intensity = Math.min(255, Math.floor(255 - Math.abs(value) * 100));
                cell.style.backgroundColor = `rgb(255, ${intensity}, ${intensity})`;
            }
            row.appendChild(cell);
        });
        table.appendChild(row);
    });
    container.appendChild(table);
}
