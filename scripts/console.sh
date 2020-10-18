#!/bin/bash

source .env

picocom $PORT -b$BAUD
