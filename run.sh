#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
echo -e "\n\n\n"
all_args=("$@")
python3 magic.py "${all_args[@]}"
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Virtual-environment: $VIRTUAL_ENV"
    exit
fi
echo "No virtual-environment"