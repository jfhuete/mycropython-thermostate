#!/bin/bash

set -e

source .env
BIN_FILES=($(ls -d firmware/*))

VENV=".venv/thermostate-device"

if ! [ -d "$VENV" ]; then
    mkdir -p .venv
    pushd .venv
    python -m venv thermostate-device
    popd
fi

source .venv/thermostate-device/bin/activate

esptool.py --port $PORT erase_flash

esptool.py --port $PORT --baud $BAUD write_flash --flash_size=detect 0 ${BIN_FILES[0]}
