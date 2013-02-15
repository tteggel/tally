#!/bin/bash

sudo apt-get update

sudo apt-get install -y python3.2 python-pip python-virtualenv

virtualenv .venv

source .venv/bin/activate

pip install -r requirements.txt

python tally.py
