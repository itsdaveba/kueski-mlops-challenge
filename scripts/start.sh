#!/bin/bash

cd /home/ec2-user/mlops
source venv/bin/activate
dvc pull data/api_dataset.pkl
dvc pull models/api.joblib
sudo unlink /tmp/supervisor.sock
supervisord -c supervisord.conf