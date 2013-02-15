#!/bin/bash

## Designed to deploy to a fresh Ubuntu 12.04 image.
## Run as root or with sudo
## You probably shouldn't run this.

add-apt-repository ppa:fkrull/deadsnakes

apt-get update

apt-get install -y python2.7 python-pip python-virtualenv libevent-dev gcc

virtualenv -p python2.7 .venv

source .venv/bin/activate

pip install -r requirements.txt

python gevent/setup.py install
