#!/bin/bash

set -e

source .env

echo "Flashing..."
scripts/flash.sh

echo "Run program"
ampy --port $PORT run -n main.py
picocom $PORT -b$BAUD