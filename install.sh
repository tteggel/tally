#!/bin/bash

## Designed to deploy to a fresh Ubuntu 12.04 image.
## Run as root or with sudo
## You probably shouldn't run this.

apt-get update

apt-get install -y build-essential python2.7 python-pip python-virtualenv libevent-dev python-dev libxml2-dev libxslt-dev

virtualenv -p python2.7 .venv

source .venv/bin/activate

./setup.py install
