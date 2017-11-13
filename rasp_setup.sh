#!/bin/bash

# Remember to make this file executable
# To do this run: chmod +x rasp_setup.sh

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (i.e. run with sudo)"
    exit
fi

setxkbmap fi
apt-get update
apt-get upgrade
cd /opt
git clone https://github.com/alexa-pi/AlexaPi.git 
./AlexaPi/src/scripts/setup.sh
systemctl start AlexaPi.service
