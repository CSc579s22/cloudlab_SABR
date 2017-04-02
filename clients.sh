#!/bin/bash
echo "This is a silly script" > /tmp/silly.txt
sudo apt-get -y --force-yes update
sudo apt-get -y --force-yes install python-pip python-dev build-essential vim screen
sudo pip install urllib3 httplib2 pymongo netifaces requests numpy sortedcontainers 
