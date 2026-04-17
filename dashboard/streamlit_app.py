import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json
import random

st.set_page_config(page_title="Retail Demand Intelligence", layout="wide")

st.title("AI Retail Demand Forecasting Platform")

# -------------------------------
# SIDEBAR INPUT
# -------------------------------

st.sidebar.header("Quick Input")

store = st.sidebar.number_input("Store ID", 1, 10, 1)
item = st.sidebar.number_input("Item ID", 1, 50, 1)

# -------------------------------
# STOCK ALERT BUTTONS (DYNAMIC STORE)
# -------------------------------

st.sidebar.subheader(f"Stock Alerts (Store {store})")

low_button = st.sidebar.button(f"Low Stock Items - Store {store}")
critical_button = st.sidebar.button(f"Critical Stock Items - Store {store}")

# -------------------------------
# AUTO FEATURE GENERATION
# -------------------------------

sales_lag_7 = random.randint(30,60)
sales_lag_14 = random.randint(25,55)
sales_lag_30 = random.randint(20,50)

rolling_mean_7 = (sales_lag_7 + sales_lag_14)/2
rolling_mean_14 = (sales_lag_14 + sales_lag_30)/2

payload = {
    "store": store,
    "item": item,
    "year": 2018,
    "month": 1,
    "day": 1,
    "day_of_week": 0,
    "week_of_year": 1,
    "sales_lag_7": sales_lag_7,
    "sales_lag_14": sales_lag_14,
    "sales_lag_30": sales_lag_30,
    "rolling_mean_7": rolling_mean_7,
    "rolling_mean_14": rolling_mean_14
}

# -------------------------------
# JSON INPUT
# -------------------------------

st.sidebar.subheader("Advanced JSON Input")

json_input = st.sidebar.text_area(
    "Paste JSON payload",
    value=json.dumps(payload, indent=2),
    height=200
)

try:

    payload = json.loads(json_input)

    response = requests.post(
        "http://127.0.0.1:8000/recommend-inventory",
        json=payload
    )

    result = response.json()
    inventory = result["inventory_recommendation"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Predicted Demand", round(inventory["predicted_demand"],2))
    col2.metric("Safety Stock", round(inventory["safety_stock"],2))
    col3.metric("Recommended Stock", round(inventory["recommended_stock"],2))
    col4.metric("Inventory Gap", round(inventory["inventory_gap"],2))

    st.subheader("Stock Risk Indicator")

    predicted = inventory["predicted_demand"]
    recommended = inventory["recommended_stock"]

    if predicted >= recommended:
        st.error("🔴 Critical Stock Level")
    elif predicted >= recommended * 0.8:
        st.warning("🟡 Low Stock Level")
    else:
        st.success("🟢 Safe Stock Level")

    chart_data = pd.DataFrame({
        "Category": ["Demand", "Safety Stock", "Recommended Stock"],
        "Units": [
            inventory["predicted_demand"],
            inventory["safety_stock"],
            inventory["recommended_stock"]
        ]
    })

    fig = px.bar(
        chart_data,
        x="Category",
        y="Units",
        text="Units",
        title="Inventory Recommendation"
    )

    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

    st.plotly_chart(fig, use_container_width=True)

except:
    st.warning("Invalid JSON or API not running.")

# --------------------------------
# STOCK ALERT RESULTS
# --------------------------------

if low_button or critical_button:

    st.divider()

    st.header(f"Store {store} Inventory Alerts")

    items = [f"Item {i}" for i in range(1,21)]
    inventory_levels = [random.randint(5,40) for _ in range(20)]

    df = pd.DataFrame({
        "Item": items,
        "Current Stock": inventory_levels
    })

    if low_button:

        low_df = df[df["Current Stock"] < 20]

        st.subheader("Low Stock Items")

        st.dataframe(low_df)

        fig = px.bar(
            low_df,
            x="Item",
            y="Current Stock",
            title="Low Stock Inventory"
        )

        st.plotly_chart(fig, use_container_width=True)

    if critical_button:

        critical_df = df[df["Current Stock"] < 10]

        st.subheader("Critical Stock Items")

        st.dataframe(critical_df)

        fig = px.bar(
            critical_df,
            x="Item",
            y="Current Stock",
            title="Critical Stock Inventory",
            color="Current Stock"
        )

        st.plotly_chart(fig, use_container_width=True)

