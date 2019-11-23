#!/bin/bash

set -e

source scripts/config

IGNORED=[".micropythonrc","scripts/flash.sh","scripts/config","scripts/run.sh","../.gitignore"]

CHANGED_FILES=`git diff HEAD --name-status --no-renames | awk '$1 != "D" {print $2}' | sed -e 's/esp3288\///g'`
DELETED_FILES=`git diff HEAD --name-status --no-renames | awk '$1 == "D" {print $2}' | sed -e 's/esp3288\///g'`

DEVICE_FILES=`ampy --port $PORT ls | sed -e 's/^\///g'`

for arg in "$@"
do
  case $arg in
    -a | --all)
      CHANGED_FILES=*
      shift
  esac
done


# Remove old files

for file in $DELETED_FILES
do
    if [[ " ${IGNORED[*]} " == *"$file"* ]] ; then
        continue;
    fi
    if [[ " ${DEVICE_FILES[*]} " == *"$file"* ]] ; then
        echo "DELETE: " $file
        ampy --port $PORT --baud $BAUD rm $file || true
    fi
done

# Upload changed and new files

for file in $CHANGED_FILES
do
    if [[ " ${IGNORED[*]} " == *"$file"* ]] ; then
        continue;
    fi
    echo "UPLOAD: " $file
    ampy --port $PORT --baud $BAUD put $file
done