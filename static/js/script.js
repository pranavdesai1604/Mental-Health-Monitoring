// static/js/script.js

document.addEventListener("DOMContentLoaded", function() {
    // Example: Add event listener to validate the form before submission
    const form = document.querySelector("form");

    form.addEventListener("submit", function(event) {
        const mood = document.getElementById("mood").value.trim();
        const activity = document.getElementById("activity").value.trim();
        const sleep = document.getElementById("sleep").value;

        if (mood === "" || activity === "" || sleep === "") {
            alert("Please fill in all fields before submitting.");
            event.preventDefault();
        }
    });
});
