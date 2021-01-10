#!/bin/bash

service=/etc/systemd/system/buildbot.service
ROOT=$(dirname "$(readlink -f "$0")")

echo "[Unit]" > $service
echo "Description=BuildBot" >> $service
echo "[Service]" >> $service
echo "ExecStart=$ROOT/start.sh" >> $service
echo "ExecStop=$ROOT/stop.sh" >> $service
echo "Type=forking" >> $service
echo "PIDFile=$ROOT/twistd.pid" >> $service
echo "WorkingDirectory=$ROOT" >> $service
echo "User=$USER" >> $service
echo "[Install]" >> $service
echo "WantedBy=multi-user.target" >> $service 

systemctl enable buildbot
systemctl daemon-reload
