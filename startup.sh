#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt -v
python3 magic.py
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Virtual-environment: $VIRTUAL_ENV"
    exit
fi
echo "No virtual-environment"