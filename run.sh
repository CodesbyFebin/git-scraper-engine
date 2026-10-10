#!/bin/bash
# Quick launcher for the Git Search Command Center
pip install -r requirements.txt -q
echo "Starting Git Search Command Center..."
echo "Open the URL shown below in your browser."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
