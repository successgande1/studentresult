// voucher.js
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("generate-voucher-form");
    const planSelect = form.querySelector("#id_plan_id");
    const durationDisplay = document.getElementById("duration-display");
    const durationInput = document.getElementById("id_duration_days");

    // Define a function to update the displayed duration and plan_id field
    function updateDurationAndPlanId() {
        const selectedOption = planSelect.options[planSelect.selectedIndex];
        const planId = selectedOption.value; // Get the plan's ID
        const planName = selectedOption.text; // Get the plan's name
        const durationDays = selectedOption.getAttribute("data-duration-days");
        durationDisplay.textContent = durationDays + " days";
        durationInput.value = durationDays; // Set the visible input value
        planSelect.value = planId; // Set the plan_id field value
    }

    // Add an event listener to the plan select element
    planSelect.addEventListener("change", updateDurationAndPlanId);

    // Call the updateDurationAndPlanId function initially to display the default duration
    updateDurationAndPlanId();
});
