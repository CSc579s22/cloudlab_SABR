#!/bin/bash
for i in `seq 1 50`;
do
        sudo mkdir /var/www/html/BigBuckBunny_2s_mod$i
        sudo ln -s /var/www/html/ftp.itec.aau.at/ /var/www/html/BigBuckBunny_2s_mod$i/ftp.itec.aau.at
done
