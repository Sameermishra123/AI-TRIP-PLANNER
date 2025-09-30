#!/bin/bash
# Start FastAPI backend in background (port 8000)
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend (port 8501)
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
