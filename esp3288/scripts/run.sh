#!/bin/bash

set -e

source scripts/config

echo "Flashing..."
scripts/flash.sh

echo "Run program"
ampy --port $PORT run -n main.py
picocom $PORT -b$BAUD