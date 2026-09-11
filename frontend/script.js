document
    .getElementById("predictionForm")
    .addEventListener("submit", async function (event) {

        event.preventDefault();

        const resultBox = document.getElementById("result");

        resultBox.innerText = "Predicting...";

        const data = {
            MedInc: parseFloat(document.getElementById("MedInc").value),
            HouseAge: parseFloat(document.getElementById("HouseAge").value),
            AveRooms: parseFloat(document.getElementById("AveRooms").value),
            AveBedrms: parseFloat(document.getElementById("AveBedrms").value),
            Population: parseFloat(document.getElementById("Population").value),
            AveOccup: parseFloat(document.getElementById("AveOccup").value),
            Latitude: parseFloat(document.getElementById("Latitude").value),
            Longitude: parseFloat(document.getElementById("Longitude").value)
        };

        try {

            const response = await fetch("/predict", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)

            });

            const result = await response.json();

            if (!response.ok) {
    const errorMessage =
        typeof result.detail === "string"
            ? result.detail
            : JSON.stringify(result.detail);

    throw new Error(errorMessage);
}
            resultBox.innerText =
                "💰 Predicted Price: $" +
                result.predicted_price_usd.toLocaleString();

        } catch (error) {

            resultBox.innerText =
                "❌ Error: " + error.message;

        }

    });