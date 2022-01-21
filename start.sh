#!/bin/bash

pip install treq --upgrade
pip install buildbot_gitea --upgrade 
BASE_DIR=$(dirname "$(readlink -f "$0")")

buildbot restart $BASE_DIR
