#!/bin/bash

sudo apt-get -y --force-yes update
sudo apt-get -y --force-yes vim screen install apache2 python-pip python-dev build-essential libssl-dev libffi-dev
sudo apt-key -y --force-yes adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927; echo \"deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse\" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list; sudo apt-get -y --force-yes update; sudo apt-get install -y --force-yes mongodb-org
sudo pip install pymongo scapy scapy_http netifaces
sudo su; cd /var/www/html; wget -r --no-parent --reject \"index.html*\" http://www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/
sudo cp /local/repository/cloudlab_SABR/server/BigBuckBunny_2s_mod* /var/www/html/www-itec.uni-klu.ac.at/ftp/datasets/DASHDataset2014/BigBuckBunny/2sec/
sudo sh create_sym.sh
