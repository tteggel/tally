from gevent import monkey; monkey.patch_all()
import bottle
from bottle import Bottle, view, static_file, redirect, abort, request
from gevent import sleep
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError, WebSocketHandler
from lxml.html import clean

from functools import wraps
import json
import argparse
import os
import logging

from tally import Tally, Tallies, KEY_SPACE
import version
import events
import config

################################################################################
# Command line config
################################################################################
parser = argparse.ArgumentParser(
    description="""Tally server (v{0}).
    Create and share a counter.""".format(version.get_version()))
parser.add_argument('-a', '--address', default='0.0.0.0',
                    help='the ip address to bind to.',
                    type=str)
parser.add_argument('-p', '--port', default=8080,
                    help='the port number to bind to.',
                    type=int)
parser.add_argument('-m', '--mongohost', default='127.0.0.1',
                    help='the hostname of the mongodb server.',
                    type=str)
parser.add_argument('-n', '--mongoport', default=27017,
                    help='the port number of the mongodb server.',
                    type=int)
args = parser.parse_args()

config.mongo.host = args.mongohost
config.mongo.port = args.mongoport

################################################################################
# Module setup
################################################################################

app = Bottle()
tallies = Tallies()
bottle.TEMPLATE_PATH.append('{0}/views'.format(os.path.dirname(__file__)))

################################################################################
# Helper functions and decorators
################################################################################

def key404(f):
    """
    Make KeyErrors return 404.
    Apply to any route or action that takes a key as parameter.
    """
    def wrapper(key=None, *a, **ka):
        try:
            return f(key=key, *a, **ka)
        except KeyError:
            return abort(404, "Key Not Found")
    return wraps(f)(wrapper)

def websocket(connect=None, message=None, error=None):
    def decorator(f):
        def wrapper(*a, **ka):
            wsock = request.environ.get('wsgi.websocket')
            if not wsock:
                # normal route execution please
                return f(*a, **ka)
            else:
                # websocket request
                try:
                    # allow the connect function to send back some
                    # arbitrary things into this scope to keep them
                    # alive for the duration of the event loop below.
                    if connect: persist = connect(wsock, *a, **ka)
                except WebSocketError as e:
                    if(error): error(wsock, e *a, **ka)

                # websocket event loop
                while True:
                    try:
                        raw = wsock.receive()
                        if raw is None: break
                        if (message): message(wsock, raw, *a, **ka)
                    except WebSocketError as e:
                        if error: error(wsock, *a, **ka)
                        break
        return wraps(f)(wrapper)
    return decorator

def _clean(html):
    return clean.clean_html(html)

################################################################################
# Websocket handlers
################################################################################

def view_tally_route_websocket_connect(wsock, key=None):
    def key_changed(tally=None):
        wsock.send(json.dumps({'message': 'changed',
                               'key': tally.key,
                               'value': tally.value}))

    events.on_value_changed(key_changed, key)

    # pub sub is weak reference so send ref of key_changed back
    # to event loop scope to keep it alive.
    return [key_changed]

def view_tally_route_websocket_message(wsock, message, key=None):
    decoded = json.loads(message)
    if('message' in decoded
       and decoded['message'] == 'inc'
       and 'key' in decoded
       and 'inc' in decoded):
        tally = tallies[decoded['key']]
        tally.inc(float(decoded['inc']))

################################################################################
# Routes
################################################################################

# base route for individual tally
key_route = '/<key:re:[' + KEY_SPACE + ']*>'

## Satic routes ################################################################

@app.route('/')
@view('index')
def index_route():
    return {'nav': True}

@app.route('/new')
@view('new')
def new_route():
    return {'page': True,
            'nav': True}

@app.route('/static/<filepath:path>')
def static_route(filepath):
    return static_file(filepath,
                       root='{0}/static'.format(os.path.dirname(__file__)))

@app.route('<filepath:path>/')
def slash_route(filepath):
    """
    Redirect routes with trailing slash to one without.
    """
    return redirect(filepath)

## Actions #####################################################################

@app.post('/new')
def new_action():
    name = desc = initial = unit = buttons = None
    if(request.forms.name): name = _clean(request.forms.name)
    if(request.forms.desc): desc = _clean(request.forms.desc)
    if(request.forms.initial): initial = float(request.forms.initial)
    if(request.forms.unit): unit = _clean(request.forms.unit)
    if(request.forms.inc): buttons = request.forms.getall('inc')
    tally = Tally(name=name, desc=desc, initial=initial,
                  unit=unit, buttons=buttons)
    tallies[tally.key] = tally
    return redirect('/' + tally.key)

@app.post(key_route + '/inc')
@key404
def inc_action(key=None):
    inc = float(request.forms.inc)
    tally = tallies[key]
    tally.inc(inc)
    return redirect('/' + tally.key)

## Dynamic routes ##############################################################

def tally_data(key):
    tally = tallies[key]
    return {'nav': True,
            'key': tally.key,
            'value': tally.value,
            'name': tally.name,
            'desc': tally.desc,
            'initial': tally.initial,
            'unit': tally.unit,
            'buttons': tally.buttons}

@app.route(key_route + "/minimal")
@websocket(connect=view_tally_route_websocket_connect,
           message=view_tally_route_websocket_message)
@view('tally')
@key404
def view_tally_minimal_route(key=None):
    data = tally_data(key)
    data['nav'] = False
    return data

@app.route(key_route)
@websocket(connect=view_tally_route_websocket_connect,
           message=view_tally_route_websocket_message)
@view('tally')
@key404
def view_tally_route(key=None):
    return tally_data(key)

################################################################################
# Main
################################################################################

def main():
    """
    Run the server.
    """
    server = WSGIServer((args.address, args.port), app,
                        handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
