#!/bin/bash

cd /home/ec2-user/mlops
source venv/bin/activate
dvc init --no-scm -f
dvc pull
uvicorn app.api:app --port 5000