#!/bin/bash

cd /home/ec2-user/mlops
source venv/bin/activate
uvicorn app.api:app --port 5000