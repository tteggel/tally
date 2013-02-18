Tally
=====

It counts stuff.

Build Status
------------
.. image:: https://travis-ci.org/thom-leggett/tally.png?branch=master

Installing
----------

To install (prefereably in a fresh virtualenv)::
  python setup.py install

Developing
----------

Tally only works with python 2.7 at the moment.

First set up and activate a lovely clean 2.7 virtualenv::
  virtualenv -p python2.7 .venv
  source .venv/bin/activate

Then install the runtime deps::
  python setup.py develop

And finally the test deps::
  pip install -r requirements.txt

Hack away. Then don't forget::
  nosetests
