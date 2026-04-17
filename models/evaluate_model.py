import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

print("Loading dataset...")

df = pd.read_csv("data/raw/train.csv")

df["date"] = pd.to_datetime(df["date"])

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["day_of_week"] = df["date"].dt.dayofweek
df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)

df = df.sort_values(["store","item","date"])

df["sales_lag_7"] = df.groupby(["store","item"])["sales"].shift(7)
df["sales_lag_14"] = df.groupby(["store","item"])["sales"].shift(14)
df["sales_lag_30"] = df.groupby(["store","item"])["sales"].shift(30)

df["rolling_mean_7"] = df.groupby(["store","item"])["sales"].transform(lambda x: x.rolling(7).mean())
df["rolling_mean_14"] = df.groupby(["store","item"])["sales"].transform(lambda x: x.rolling(14).mean())

df = df.dropna()

print("Loading model...")

model = joblib.load("models/retail_demand_model.pkl")

features = [
"store","item","year","month","day",
"day_of_week","week_of_year",
"sales_lag_7","sales_lag_14","sales_lag_30",
"rolling_mean_7","rolling_mean_14"
]

X = df[features]
y = df["sales"]

print("Generating predictions...")

preds = model.predict(X)

mae = mean_absolute_error(y, preds)
rmse = np.sqrt(mean_squared_error(y, preds))

# FIXED MAPE
mask = y != 0
mape = np.mean(np.abs((y[mask] - preds[mask]) / y[mask])) * 100

print()
print("Model Evaluation Results")
print("------------------------")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"MAPE : {mape:.2f}%")
