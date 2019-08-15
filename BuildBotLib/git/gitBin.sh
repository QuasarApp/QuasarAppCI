#!/bin/bash

[ "${1}" = "log" ] && { shift && git log --ignore-missing "${@}"; } || git "${@}"
