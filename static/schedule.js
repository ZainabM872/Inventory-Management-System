document.addEventListener("DOMContentLoaded", function() {
    // Number of dots to display for each day (you can modify these values)
    const dotsData = {
        1: 2,  // Day 1 has 2 dots
        2: 1,  // Day 2 has 1 dot
        3: 3,  // Day 3 has 3 dots
        4: 1,  // Day 4 has 1 dot
        5: 2,  // Day 5 has 2 dots
        6: 0,  // Day 6 has no dots
        7: 4,  // Day 7 has 4 dots
        8: 3,  // Day 8 has 3 dots
        9: 2,  // Day 9 has 2 dots
        10: 1, // Day 10 has 1 dot
    };

    const colours = [
        '#d28a8c',  // Red
        '#a7c8b4',  // Dark Green
        '#e0d59d',  // Dark Yellow
        '#e0a1b6',  // Dark Pink
        '#a1c3d5',  // Dark Blue
        '#e6b69f',  // Dark Orange
        '#bcb0d5',  // Dark Purple
    ];

    // Loop through each day in the calendar
    const days = document.querySelectorAll('.calendar .days li');
    days.forEach(day => {
        // Get the day number from the text content (skip inactive days)
        const dayNumber = parseInt(day.textContent.trim());
        
        if (!isNaN(dayNumber)) {
            // Create a div for dots
            const dotsDiv = document.createElement('div');
            dotsDiv.classList.add('dots');

            // Get the number of dots to display for this day
            const numDots = dotsData[dayNumber] || 0;

            // Add the dots to the div
            for (let i = 0; i < numDots; i++) {
                const dot = document.createElement('span');
                dot.style.display = 'inline-block';  // Make sure it behaves like an inline element
                dot.style.width = '10px';  // Set the diameter of the circle
                dot.style.height = '10px';  // Set the diameter of the circle
                dot.style.borderRadius = '50%';  // Make it circular
                dot.style.backgroundColor = colours[Math.floor(Math.random() * colours.length)];  // Set the color randomly
                dot.style.fontSize = '15px';  // Set the font size
                dot.style.marginRight = '5px';  // Space between circles
                dotsDiv.appendChild(dot);
            }

            // Append the dots div to the current day
            day.appendChild(dotsDiv);
        }
    });
});
