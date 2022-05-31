#!/bin/bash

sudo pip3 install virtualenv
cd /home/ec2-user/mlops
virtualenv venv
source venv/bin/activate
sudo pip3 install dvc[gdrive]
sudo pip3 install -r api-requirements.txt
sudo amazon-linux-extras install docker -y
sudo service docker start