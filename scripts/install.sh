#!/bin/bash

cd /home/ec2-user/mlops
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
dvc pull