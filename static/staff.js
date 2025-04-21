const schedule = [
    {
        day: "Sunday",
        date: "13",
        shifts: []
    },
    {
        day: "Monday",
        date: "14",
        shifts: [
            "8:00 AM – 12:00 PM [4h]: 7063 - Store 021 - Server",
            "1:00 PM – 5:00 PM [4h]: 7063 - Store 021 - Cashier"
        ]
    },
    {
        day: "Tuesday",
        date: "15",
        shifts: [
            "1:00 PM – 9:30 PM [8.5h]: 7063 - Store 021 - Server/Cashier"
        ]
    },
    {
        day: "Wednesday",
        date: "16",
        shifts: []
    },
    {
        day: "Thursday",
        date: "17",
        shifts: [
            "9:00 AM – 12:00 PM [3h]: 7063 - Store 021 - Cashier"
        ]
    },
    {
        day: "Friday",
        date: "18",
        shifts: [
            "10:00 PM – 2:00 AM [4h]: 7063 - Store 021 - Night Shift"
        ]
    },
    {
        day: "Saturday",
        date: "19",
        shifts: []
    }
];

const container = document.getElementById("calendar-container");

schedule.forEach(entry => {
    const row = document.createElement("div");
    row.className = "day-row";

    const dayInfo = document.createElement("div");
    dayInfo.className = "day-info";
    dayInfo.innerHTML = `
        <div class="day">${entry.day}</div>
        <div class="date">${entry.date}</div>
    `;

    const shiftInfo = document.createElement("div");
    shiftInfo.className = "shift-info";

    if (entry.shifts.length === 0) {
        shiftInfo.innerHTML = "<span><em>Off</em></span>";
    } else {
        entry.shifts.forEach(shift => {
            const shiftLine = document.createElement("span");
            shiftLine.textContent = shift;
            shiftInfo.appendChild(shiftLine);
        });
    }

    row.appendChild(dayInfo);
    row.appendChild(shiftInfo);
    container.appendChild(row);
});
