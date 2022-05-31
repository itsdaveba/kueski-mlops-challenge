#!/bin/bash

cd /home/ec2-user/mlops
source venv/bin/activate
dvc pull data/api_dataset.pkl
dvc pull models/api.joblib
sudo service docker start
docker build -t mlops:latest .
docker run -d -p 5000:80 --name mlops mlops:latest