#!/bin/bash

## Designed to deploy to a fresh Ubuntu 12.04 image.
## Run as root or with sudo
## You probably shouldn't run this.

apt-get update

apt-get install -y python3.2 python-pip python-virtualenv

virtualenv .venv

source .venv/bin/activate

pip install -r requirements.txt
