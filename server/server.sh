#!/bin/bash

sudo apt-get -y --force-yes update
sudo apt-get -y --force-yes install vim screen apache2 python-pip python-dev build-essential libssl-dev libffi-dev
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6; echo "deb [ arch=amd64 ] http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list; sudo apt-get -y --force-yes update; sudo apt-get install -y --force-yes mongodb-org
sudo pip install pymongo scapy scapy_http netifaces
sudo su; cd /var/www/html; wget -r --no-parent --reject \"index.html*\" http://www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/
sudo cp /local/repository/server/BigBuckBunny_2s_mod* /var/www/html/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/
sudo sh create_sym.sh
