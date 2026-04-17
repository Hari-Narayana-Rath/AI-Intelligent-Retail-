import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from models.predict import predict_demand
from models.inventory_optimizer import calculate_inventory_recommendation

app = FastAPI(title="Retail Demand Forecast API")


class DemandRequest(BaseModel):
    store: int
    item: int
    year: int
    month: int
    day: int
    day_of_week: int
    week_of_year: int
    sales_lag_7: float
    sales_lag_14: float
    sales_lag_30: float
    rolling_mean_7: float
    rolling_mean_14: float


@app.get("/")
def home():
    return {"message": "Retail Demand Forecast API running"}


@app.post("/predict-demand")
def predict(request: DemandRequest):

    data = pd.DataFrame([request.dict()])
    prediction = predict_demand(data)

    result = prediction["predicted_sales"].iloc[0]

    return {
        "store": request.store,
        "item": request.item,
        "predicted_sales": float(result)
    }


@app.post("/recommend-inventory")
def recommend_inventory(request: DemandRequest):

    data = pd.DataFrame([request.dict()])
    prediction = predict_demand(data)

    predicted_sales = prediction["predicted_sales"].iloc[0]

    inventory = calculate_inventory_recommendation(predicted_sales)

    return {
        "store": request.store,
        "item": request.item,
        "inventory_recommendation": inventory
    }
