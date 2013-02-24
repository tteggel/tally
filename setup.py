#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

from tally.version import get_version

readme = open('README.rst').read()

long_description = readme

setup(
    name='Tally',
    version=get_version(),
    description='Tally is for counting things',
    long_description=long_description,
    author='Thom Leggett',
    author_email='thom@tteggel.org',
    url='http://tally.tteggel.org',
    packages=['tally', 'tally.test'],
    test_suite='tally.test',
    tests_require=['nose',
                   'ws4py>=0.2.4',
                   'requests>=1.1.0',
                   'webtest>=1.4.3'],
    install_requires=['bottle==0.11.6',
                      'gevent==0.13.8',
                      'gevent-websocket==0.3.6',
                      'pypubsub==3.1.2',
                      'lxml==3.1.0',
                      'pymongo==2.4.2'],
    entry_points={
        'console_scripts': [
            'tally = tally.server:main',
        ]
    },
    zip_safe=False,
    include_package_data=True,
    classifiers=[
    ],
)
