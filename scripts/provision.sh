#!/bin/bash

set -e

VENV=".venv/thermostate-device"

if ! [ -d "$VENV" ]; then
    mkdir -p .venv
    pushd .venv
    python -m venv thermostate-device
    popd
fi

source .venv/thermostate-device/bin/activate

pip install -r requirements.txt

sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install picocom
