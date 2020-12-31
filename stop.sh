#~/bin/bash
BASE_DIR=$(dirname "$(readlink -f "$0")")

buildbot stop $BASE_DIR

