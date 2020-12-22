#!/bin/bash

service=/etc/systemd/system/buildbot.service
ROOT=BASE_DIR=$(dirname "$(readlink -f "$0")")

echo "[Unit]" >> $service
echo "Description=BuildBot" >> $service
echo "[Service]" >> $service
echo "ExecStart=$ROOT/start.sh" >> $service
echo "Type=forking" >> $service
echo "PIDFile=$ROOT/twistd.pid" >> $service
echo "[Install]" >> $service
echo "WantedBy=multi-user.target" >> $service 

