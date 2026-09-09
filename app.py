from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model and scaler
model = joblib.load("linear_regression_model.pkl")
scaler = joblib.load("scaler.pkl")


# Exact feature order used during model training
FEATURE_COLUMNS = [
    "Outdoor Temperature (°C)",
    "Household Size",
    "Season_Spring",
    "Season_Summer",
    "Season_Winter",
    "Appliance Type_Computer",
    "Appliance Type_Dishwasher",
    "Appliance Type_Fridge",
    "Appliance Type_Heater",
    "Appliance Type_Lights",
    "Appliance Type_Microwave",
    "Appliance Type_Oven",
    "Appliance Type_TV",
    "Appliance Type_Washing Machine",
    "Year",
    "Month",
    "Day",
    "DayOfWeek",
    "Hour",
    "Minute"
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        # -------------------------
        # Get input values
        # -------------------------
        temperature = float(data["temperature"])
        household_size = int(data["household_size"])
        season = data["season"]
        appliance = data["appliance"]
        date = pd.to_datetime(data["date"])
        time = pd.to_datetime(data["time"], format="%H:%M")

        # -------------------------
        # Date features
        # -------------------------
        year = date.year
        month = date.month
        day = date.day
        day_of_week = date.dayofweek

        # -------------------------
        # Time features
        # -------------------------
        hour = time.hour
        minute = time.minute

        # -------------------------
        # Initialize all features
        # -------------------------
        input_data = {
            "Outdoor Temperature (°C)": temperature,
            "Household Size": household_size,

            "Season_Spring": 0,
            "Season_Summer": 0,
            "Season_Winter": 0,

            "Appliance Type_Computer": 0,
            "Appliance Type_Dishwasher": 0,
            "Appliance Type_Fridge": 0,
            "Appliance Type_Heater": 0,
            "Appliance Type_Lights": 0,
            "Appliance Type_Microwave": 0,
            "Appliance Type_Oven": 0,
            "Appliance Type_TV": 0,
            "Appliance Type_Washing Machine": 0,

            "Year": year,
            "Month": month,
            "Day": day,
            "DayOfWeek": day_of_week,
            "Hour": hour,
            "Minute": minute
        }

        # -------------------------
        # Season encoding
        # -------------------------
        if season == "Spring":
            input_data["Season_Spring"] = 1

        elif season == "Summer":
            input_data["Season_Summer"] = 1

        elif season == "Winter":
            input_data["Season_Winter"] = 1

        # Fall is the dropped/base category
        # Therefore all season dummy columns remain 0

        # -------------------------
        # Appliance encoding
        # -------------------------
        appliance_column = f"Appliance Type_{appliance}"

        if appliance_column in input_data:
            input_data[appliance_column] = 1

        # Air Conditioning is the dropped/base category
        # Therefore all appliance dummy columns remain 0

        # -------------------------
        # Create DataFrame
        # -------------------------
        input_df = pd.DataFrame([input_data])

        # Make absolutely sure feature order is correct
        input_df = input_df[FEATURE_COLUMNS]

        # -------------------------
        # Scale input
        # -------------------------
        input_scaled = scaler.transform(input_df)

        # -------------------------
        # Prediction
        # -------------------------
        prediction = model.predict(input_scaled)[0]

        # Electricity consumption cannot be negative
        prediction = max(0, prediction)

        return jsonify({
            "success": True,
            "prediction": round(float(prediction), 3)
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)