#!/bin/bash
sudo apt-get update
sudo apt-get install -y python3-pip
sudo apt-get install -y unzip
pip3 install pyTelegramBotAPI
pip3 install bs4
pip3 install lxml
pip3 install selenium
pip3 install geopy
cd /home
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
wget https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /home
