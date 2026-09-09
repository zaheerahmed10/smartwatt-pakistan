const form = document.getElementById("predictionForm");

const dateInput = document.getElementById("date");
const timeInput = document.getElementById("time");

const seasonInput = document.getElementById("season");
const seasonButtons = document.querySelectorAll(".season-btn");

const seasonMessage = document.getElementById("seasonMessage");

const predictBtn = document.getElementById("predictBtn");
const buttonText = document.getElementById("buttonText");
const loader = document.getElementById("loader");

const predictionValue = document.getElementById("predictionValue");
const resultText = document.getElementById("resultText");

const errorCard = document.getElementById("errorCard");
const errorText = document.getElementById("errorText");


// -----------------------------
// CURRENT DATE & TIME
// -----------------------------

function setCurrentDateTime() {

    const now = new Date();

    const year = now.getFullYear();

    const month = String(now.getMonth() + 1).padStart(2, "0");

    const day = String(now.getDate()).padStart(2, "0");

    const hours = String(now.getHours()).padStart(2, "0");

    const minutes = String(now.getMinutes()).padStart(2, "0");

    dateInput.value = `${year}-${month}-${day}`;

    timeInput.value = `${hours}:${minutes}`;
}

setCurrentDateTime();


// -----------------------------
// SEASON
// -----------------------------

function getSeason(dateString) {

    const date = new Date(dateString);

    const month = date.getMonth() + 1;

    if (month >= 3 && month <= 5) {
        return "Spring";
    }

    if (month >= 6 && month <= 8) {
        return "Summer";
    }

    if (month >= 9 && month <= 11) {
        return "Fall";
    }

    return "Winter";
}


// -----------------------------
// SELECT SEASON
// -----------------------------

function selectSeason(season) {

    seasonInput.value = season;

    seasonButtons.forEach(button => {

        button.classList.remove("active");

        if (button.dataset.season === season) {
            button.classList.add("active");
        }

    });

    seasonMessage.innerHTML = `
        <i class="fa-solid fa-circle-check"></i>
        ${season} selected.
    `;
}


// -----------------------------
// AUTO SEASON FROM DATE
// -----------------------------

function updateSeasonFromDate() {

    if (!dateInput.value) {
        return;
    }

    const season = getSeason(dateInput.value);

    selectSeason(season);
}

dateInput.addEventListener("change", updateSeasonFromDate);


// -----------------------------
// MANUAL SEASON BUTTON
// -----------------------------

seasonButtons.forEach(button => {

    button.addEventListener("click", () => {

        selectSeason(button.dataset.season);

    });

});


// -----------------------------
// ERROR
// -----------------------------

function showError(message) {

    errorText.textContent = message;

    errorCard.style.display = "flex";

}

function hideError() {

    errorCard.style.display = "none";

}


// -----------------------------
// LOADING
// -----------------------------

function setLoading(isLoading) {

    if (isLoading) {

        predictBtn.disabled = true;

        buttonText.style.display = "none";

        loader.style.display = "block";

    } else {

        predictBtn.disabled = false;

        buttonText.style.display = "inline";

        loader.style.display = "none";

    }

}


// -----------------------------
// FORM SUBMIT
// -----------------------------

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    hideError();

    const temperature =
        parseFloat(
            document.getElementById("temperature").value
        );

    const household =
        parseInt(
            document.getElementById("household").value
        );

    const appliance =
        document.getElementById("appliance").value;

    const date =
        dateInput.value;

    const time =
        timeInput.value;

    const season =
        seasonInput.value;


    // Validation

    if (isNaN(temperature)) {

        showError("Please enter a valid temperature.");

        return;
    }


    if (isNaN(household) || household < 1) {

        showError("Please enter a valid household size.");

        return;
    }


    if (!appliance) {

        showError("Please select an appliance.");

        return;
    }


    if (!date || !time) {

        showError("Please select date and time.");

        return;
    }


    if (!season) {

        showError("Please select a season.");

        return;
    }


    setLoading(true);


    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                temperature: temperature,

                household_size: household,

                appliance: appliance,

                date: date,

                time: time,

                season: season

            })

        });


        const data = await response.json();


        if (!response.ok || data.error) {

            throw new Error(
                data.error || "Prediction failed."
            );

        }


        // Display prediction

        predictionValue.textContent =
            Number(data.prediction).toFixed(3);


        resultText.textContent =
            `Estimated electricity consumption for the selected conditions is ${Number(data.prediction).toFixed(3)} kWh.`;


        // Smooth scroll to result

        document
            .getElementById("resultCard")
            .scrollIntoView({
                behavior: "smooth",
                block: "center"
            });


    } catch (error) {

        showError(error.message);

    } finally {

        setLoading(false);

    }

});