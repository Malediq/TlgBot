#!/bin/bash
echo "Enter filepath to TlgBot folder"
read Filepath
cd $Filepath
touch /etc/cron.d/CheckEvent
echo "* * * * * root ${Filepath}/Check_Event.py" > /etc/cron.d/CheckEvent
echo "Enter your your chat id"
read botid
echo "Enter your timedelta between hostserver and client in hours"
read timed
echo "Enter your dollar exchange rate"
read kp
echo "Enter number of dollars"
read dollarsum
if [ "$botid" != '' ]; then
        sed -i "s|chatid=[a-zA-Z_]*|chatid=${botid}|" value.py
fi
if [ "$timed" != '' ]; then
        sed -i "s|timed=[a-zA-Z_]*|timed=${timed}|" value.py
fi
if [ "$kp" != '' ]; then
        sed -i "s|kp=[a-zA-Z_]*|kp=${kp}|" value.py
fi
if [ "$dollarsum" != '' ]; then
        sed -i "s|dollarsumm=[a-zA-Z_]*|dollarsumm=${dollarsum}|" value.py
fi
service bot restart
