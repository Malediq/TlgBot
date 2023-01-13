#!/bin/bash
echo "Enter filepath to TlgBot folder"
read Filepath
cd $Filepath
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get update
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y
sudo apt-get install -y python3-pip
sudo apt-get install -y unzip
pip3 install pyTelegramBotAPI
pip3 install bs4
pip3 install lxml
pip3 install selenium
pip3 install geopy
sed -i 's|<PATH>|$Filepath|' bot.service
cp bot.service /etc/systemd/system/bot.service
chmod 664 /etc/systemd/system/bot.service
sed -i 's|/home|$Filepath|g' value.py
echo "Enter your Bot id"
read Botid
sed -i 's|telebot.TeleBot('')|telebot.TeleBot('$Botid')|' value.py
service bot start
service bot status
google-chrome-stable --version
