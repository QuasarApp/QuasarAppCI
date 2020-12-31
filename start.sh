#!/bin/bash

#pip install treq
BASE_DIR=$(dirname "$(readlink -f "$0")")

buildbot start $BASE_DIR
