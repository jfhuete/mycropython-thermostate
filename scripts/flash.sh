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

CHANGED_FILES=`git diff HEAD --name-status --no-renames | grep src/ | awk '$1 != "D" {print $2}' | sed -e 's/src\///g'`
DELETED_FILES=`git diff HEAD --name-status --no-renames | grep src/ | awk '$1 == "D" {print $2}' | sed -e 's/src\///g'`

DEVICE_FILES=`ampy --port $PORT ls | sed -e 's/^\///g'`

for arg in "$@"
do
  case $arg in
    -a | --all)
        # Delete all files

        for file in $(ampy --port $PORT --baud $BAUD ls -r)
        do
            echo "DELETE: " $file
            ampy --port $PORT --baud $BAUD rm $file
        done

        # Delete all dirs
        for dir in $(ampy --port $PORT --baud $BAUD ls)
        do
            echo "DELETE: " $dir
            ampy --port $PORT --baud $BAUD rmdir $dir
        done

        # Upload code to board

        # Upload directories to board

        echo "UPLOAD DIRS"
        ampy --port $PORT --baud $BAUD put src .

        for file in $(ls -d src/*)
        do
            if [ -f "$file" ]; then
                echo "UPLOAD: " $file
                ampy --port $PORT --baud $BAUD put $file
            fi
        done
        shift
  esac
done

# Remove old files

for file in $DELETED_FILES
do
    if [[ " ${DEVICE_FILES[*]} " == *"$file"* ]] ; then
        echo "DELETE: " $file
        ampy --port $PORT --baud $BAUD rm $file || true
    fi
done

# Upload changed and new files

for file in $CHANGED_FILES
do
    echo "UPLOAD: " $file
    ampy --port $PORT --baud $BAUD put ./src/$file $file
done