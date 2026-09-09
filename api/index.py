from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import os


# =========================================================
# Flask App
# =========================================================

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


# =========================================================
# Project Root Directory
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# =========================================================
# Load Trained ML Model and Scaler
# =========================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "linear_reg.pkl"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "scaler.pkl"
)


model = joblib.load(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)


# =========================================================
# Exact Feature Order Used During Model Training
# =========================================================

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


# =========================================================
# Home Page
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# Prediction API
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # -------------------------------------------------
        # Get JSON data from frontend
        # -------------------------------------------------

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No input data received."
            }), 400


        # -------------------------------------------------
        # Get Input Values
        # -------------------------------------------------

        temperature = float(
            data["temperature"]
        )

        household_size = int(
            data["household_size"]
        )

        season = str(
            data["season"]
        )

        appliance = str(
            data["appliance"]
        )

        date = pd.to_datetime(
            data["date"]
        )

        time = pd.to_datetime(
            data["time"],
            format="%H:%M"
        )


        # -------------------------------------------------
        # Extract Date Features
        # -------------------------------------------------

        year = date.year

        month = date.month

        day = date.day

        day_of_week = date.dayofweek


        # -------------------------------------------------
        # Extract Time Features
        # -------------------------------------------------

        hour = time.hour

        minute = time.minute


        # =================================================
        # Initialize All Features
        # =================================================

        input_data = {

            "Outdoor Temperature (°C)": temperature,

            "Household Size": household_size,


            # Season
            "Season_Spring": 0,
            "Season_Summer": 0,
            "Season_Winter": 0,


            # Appliance
            "Appliance Type_Computer": 0,
            "Appliance Type_Dishwasher": 0,
            "Appliance Type_Fridge": 0,
            "Appliance Type_Heater": 0,
            "Appliance Type_Lights": 0,
            "Appliance Type_Microwave": 0,
            "Appliance Type_Oven": 0,
            "Appliance Type_TV": 0,
            "Appliance Type_Washing Machine": 0,


            # Date
            "Year": year,
            "Month": month,
            "Day": day,
            "DayOfWeek": day_of_week,


            # Time
            "Hour": hour,
            "Minute": minute
        }


        # =================================================
        # Season Encoding
        # =================================================

        if season == "Spring":

            input_data["Season_Spring"] = 1

        elif season == "Summer":

            input_data["Season_Summer"] = 1

        elif season == "Winter":

            input_data["Season_Winter"] = 1

        elif season == "Fall":

            # Fall is the base/dropped category.
            # Therefore all season dummy variables stay 0.

            pass

        else:

            return jsonify({
                "success": False,
                "error": "Invalid season selected."
            }), 400


        # =================================================
        # Appliance Encoding
        # =================================================

        appliance_column = (
            f"Appliance Type_{appliance}"
        )


        if appliance_column in input_data:

            input_data[appliance_column] = 1


        elif appliance == "Air Conditioning":

            # Air Conditioning is the base/dropped category.
            # Therefore all appliance dummy variables stay 0.

            pass

        else:

            return jsonify({
                "success": False,
                "error": "Invalid appliance selected."
            }), 400


        # =================================================
        # Create DataFrame
        # =================================================

        input_df = pd.DataFrame(
            [input_data]
        )


        # -------------------------------------------------
        # Ensure Exact Feature Order
        # -------------------------------------------------

        input_df = input_df[
            FEATURE_COLUMNS
        ]


        # =================================================
        # Scale Input
        # =================================================

        input_scaled = scaler.transform(
            input_df
        )


        # =================================================
        # Make Prediction
        # =================================================

        prediction = model.predict(
            input_scaled
        )[0]


        # -------------------------------------------------
        # Electricity Consumption Cannot Be Negative
        # -------------------------------------------------

        prediction = max(
            0,
            prediction
        )


        # =================================================
        # Return Prediction
        # =================================================

        return jsonify({

            "success": True,

            "prediction": round(
                float(prediction),
                3
            )
        })


    # =====================================================
    # Missing Input Error
    # =====================================================

    except KeyError as e:

        return jsonify({

            "success": False,

            "error": (
                f"Missing input field: {str(e)}"
            )

        }), 400


    # =====================================================
    # Invalid Input Error
    # =====================================================

    except ValueError as e:

        return jsonify({

            "success": False,

            "error": (
                f"Invalid input value: {str(e)}"
            )

        }), 400


    # =====================================================
    # General Error
    # =====================================================

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =========================================================
# Local Development
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )