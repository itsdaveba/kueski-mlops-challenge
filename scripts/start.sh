#!/bin/bash

cd /home/ec2-user/mlops
source venv/bin/activate
dvc pull models/api.joblib
uvicorn app.api:app --port 5000