# AI Retail Intelligence Platform

This project is a small end-to-end retail demand forecasting prototype built with FastAPI and Streamlit.

It predicts item demand for a store-item pair using calendar features, lagged sales, and rolling averages, then converts the forecast into an inventory recommendation.

## Included

- FastAPI app for prediction and inventory recommendation
- Streamlit dashboard for interactive exploration
- Batch prediction pipeline
- Sample raw and processed data files
- Trained model artifacts required to run the demo locally

## Project Structure

- `api/` API endpoints
- `dashboard/` Streamlit app
- `models/` prediction, evaluation, and inventory logic
- `pipelines/` batch prediction pipeline
- `data/raw/` source CSV files
- `data/processed/` sample input and prediction output

## Run Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the API and dashboard:

```powershell
./run_platform.ps1
```

3. Or start them manually:

```bash
uvicorn api.app:app --reload
streamlit run dashboard/streamlit_app.py
```

## Verify

Run the batch pipeline:

```bash
python pipelines/prediction_pipeline.py
```

Run the evaluation script:

```bash
python models/evaluate_model.py
```
