#!/bin/bash

PORT=/dev/ttyUSB0
BAUD=115200

IGNORED=[".micropythonrc","flash.sh"]

for file in *
do
    if [[ " ${IGNORED[*]} " == *"$file"* ]] ; then
        continue;
    fi
    ampy --port $PORT --baud $BAUD put $file
done