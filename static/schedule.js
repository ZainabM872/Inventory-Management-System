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

    for (let day = 1; day <= daysInMonth; day++) {
        let dayCell = document.createElement("div"); // for each day, create a new calendar cell
        dayCell.classList.add("calendar-day");
        dayCell.textContent = day; // set the current day as the content in the cell

        if (day === today.getDate()) {
            dayCell.classList.add("today"); //set the day to today if its the current date
        }

        // Randomly assign 0-3 colored dots for staff members
        let numDots = Math.floor(Math.random() * 4);
        for (let j = 0; j < numDots; j++) {
            let dot = document.createElement("div");
            dot.classList.add("dot", colors[Math.floor(Math.random() * colors.length)]);
            dayCell.appendChild(dot);
        }

        calendar.appendChild(dayCell);
    }
});