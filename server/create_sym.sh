#!/bin/bash
for i in `seq 1 50`;
do
        sudo mkdir /var/www/html/BigBuckBunny_2s_mod$i
        sudo ln -s /var/www/html/www-itec.uni-klu.ac.at/ /var/www/html/BigBuckBunny_2s_mod$i/www-itec.uni-klu.ac.at
done
