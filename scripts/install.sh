#!/bin/bash

cd /home/ec2-user/mlops
python3 -m venv venv
source venv/bin/activate
pip install -r api-requirements.txt