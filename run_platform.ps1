Start-Process powershell -ArgumentList "uvicorn api.app:app --reload"
Start-Sleep -Seconds 2
Start-Process powershell -ArgumentList "streamlit run dashboard/streamlit_app.py"
