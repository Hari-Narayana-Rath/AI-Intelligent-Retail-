import joblib
import pandas as pd

# Load trained model and feature list
model = joblib.load("models/retail_demand_model.pkl")
features = joblib.load("models/model_features.pkl")


def predict_demand(input_data: pd.DataFrame):
    """
    Predict retail demand using the trained model
    """

    # Select required features
    X = input_data[features]

    # Generate predictions
    predictions = model.predict(X)

    # Attach predictions to dataframe
    input_data["predicted_sales"] = predictions

    return input_data
