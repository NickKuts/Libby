#!/bin/bash

setxkbmap fi
apt-get update
apt-get upgrade
cd /opt
git clone https://github.com/alexa-pi/AlexaPi.git 
./AlexaPi/src/scripts/setup.sh
systemctl start AlexaPi.service
