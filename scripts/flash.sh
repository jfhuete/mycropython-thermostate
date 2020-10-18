#!/bin/bash

set -e

source .env

if ! [ -d "$VENV" ]; then
    mkdir -p .venv
    pushd .venv
    python -m venv $VENV_NAME
    popd
fi

source $VENV/bin/activate

# Delete all files

for file in $(ampy --port $PORT --baud $BAUD ls -r)
do
    ampy --port $PORT --baud $BAUD rm $file
done

# Delete all dirs

for dir in $(ampy --port $PORT --baud $BAUD ls)
do
    ampy --port $PORT --baud $BAUD rmdir $dir
done

# Upload code to board

# Upload directories to board

ampy --port $PORT --baud $BAUD put src .

for file in $(ls -d src/*)
do
    if [ -f "$file" ]; then
        ampy --port $PORT --baud $BAUD put $file
    fi
done