FROM python:3.9-slim

# Copy files
WORKDIR /mlops
COPY api-requirements.txt requirements.txt
COPY app/api.py app/api.py
COPY config/config.py config/config.py
COPY data/api_dataset.pkl data/api_dataset.pkl
COPY models/api.joblib models/api.joblib

# Install requirements
RUN python -m pip install --no-cache-dir -r requirements.txt

# Start API server
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]