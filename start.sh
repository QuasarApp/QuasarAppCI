#!/bin/bash

pip install treq
pip install buildbot_gitea
BASE_DIR=$(dirname "$(readlink -f "$0")")

buildbot start $BASE_DIR
