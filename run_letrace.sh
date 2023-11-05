#!/bin/bash

cd src
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
PYTHON_SCRIPT="$SCRIPT_DIR/main.py"

pkexec python3 "$PYTHON_SCRIPT"