import joblib
import os
import numpy as np
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request

app = Flask(__name__)

loaded_model = joblib.load(MODEL_OUTPUT_PATH)

# ------------------------------------------------------------------
# Encoding maps — these must match EXACTLY how each column was
# encoded when you trained the model (e.g. LabelEncoder.classes_,
# sorted alphabetically by default). Print each encoder's .classes_
# during training and confirm these dictionaries match that order.
# ------------------------------------------------------------------

MONTH_MAP = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

MARKET_SEGMENT_MAP = {
    "Aviation": 0,
    "Complimentary": 1,
    "Corporate": 2,
    "Offline": 3,
    "Online": 4
}

MEAL_PLAN_MAP = {
    "Meal Plan 1": 0,
    "Meal Plan 2": 1,
    "Meal Plan 3": 2,
    "Not Selected": 3
}

ROOM_TYPE_MAP = {
    "Room Type 1": 0,
    "Room Type 2": 1,
    "Room Type 3": 2,
    "Room Type 4": 3,
    "Room Type 5": 4,
    "Room Type 6": 5,
    "Room Type 7": 6
}


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", prediction=None)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        lead_time = int(request.form["lead_time"])
        no_of_special_request = int(request.form["no_of_special_request"])
        avg_price_per_room = float(request.form["avg_price_per_room"])

        # These three arrive from the form as text labels, not numbers,
        # so they go through the maps above before reaching the model.
        arrival_month = MONTH_MAP[request.form["arrival_month"]]
        market_segment_type = MARKET_SEGMENT_MAP[request.form["market_segment_type"]]
        type_of_meal_plan = MEAL_PLAN_MAP[request.form["type_of_meal_plan"]]
        room_type_reserved = ROOM_TYPE_MAP[request.form["room_type_reserved"]]

        arrival_date = int(request.form["arrival_date"])
        no_of_week_nights = int(request.form["no_of_week_nights"])
        no_of_weekend_nights = int(request.form["no_of_weekend_nights"])

        # Column order MUST match the order used during training.
        features = np.array([[
            lead_time,
            no_of_special_request,
            avg_price_per_room,
            arrival_month,
            arrival_date,
            market_segment_type,
            no_of_week_nights,
            no_of_weekend_nights,
            type_of_meal_plan,
            room_type_reserved
        ]])

        prediction = loaded_model.predict(features)

        return render_template('index.html', prediction=int(prediction[0]))

    except KeyError as e:
        return render_template('index.html', prediction=None, error=f"Missing form field: {e}")
    except ValueError as e:
        return render_template('index.html', prediction=None, error=f"Invalid value: {e}")


if __name__ == "__main__":
    # If an environment variable 'PORT' exists (like on Render), use it. 
    # Otherwise, default to 8080 so it runs locally.
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)