import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from models.predict import predict_demand


def run_prediction_pipeline(input_file: str, output_file: str):
    """
    End-to-end prediction pipeline
    """

    print("Loading input data...")
    data = pd.read_csv(input_file)

    print("Generating predictions...")
    predictions = predict_demand(data)

    print("Saving predictions...")
    predictions.to_csv(output_file, index=False)

    print("Prediction pipeline completed.")


if __name__ == "__main__":

    input_path = "data/processed/prediction_input.csv"
    output_path = "data/processed/demand_predictions.csv"

    run_prediction_pipeline(input_path, output_path)
