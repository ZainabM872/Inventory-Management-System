document.addEventListener("DOMContentLoaded", function () {
    const calendar = document.getElementById("calendar"); // get the calendar div
    const monthYear = document.getElementById("month-year"); // get the month-year div

    const today = new Date(); // get todays date to start the calendar from
    const currentYear = today.getFullYear(); // get current year
    const currentMonth = today.getMonth(); // get current month

    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ] // store the months in an array

    // Update header with current month and year
    monthYear.textContent = `${monthNames[currentMonth]} ${currentYear}`;

    // Colors for staff members
    const colors = ["red", "blue", "green", "yellow", "purple"];

    // Generate calendar days
    for (let i = 0; i < firstDay; i++) {
        let emptyCell = document.createElement("div");
        calendar.appendChild(emptyCell);
    }

});