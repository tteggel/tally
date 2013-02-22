import bottle
from bottle import Bottle, view, static_file, redirect, abort, request
from gevent import sleep
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError, WebSocketHandler
from lxml.html import clean

from pubsub import pub
import json
import argparse
import os
from functools import wraps
import logging

from tally import Tally, Tallies, KEY_SPACE
import version

tallies = Tallies()
app = Bottle()

bottle.TEMPLATE_PATH.append('{0}/views'.format(os.path.dirname(__file__)))

def key404(f):
    """
    Make KeyErrors return 404.
    Apply to any route or action that takes a key as parameter.
    """
    def wrapper(*a, **ka):
        try:
            return f(*a, **ka)
        except KeyError:
            return abort(404, "Key Not Found")
    return wraps(f)(wrapper)

def websocket(connect=None, message=None, error=None):
    def decorator(f):
        def wrapped(*a, **ka):
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
        return wraps(f)(wrapped)
    return decorator

@app.route('/')
@view('index')
def index_route():
    return {}

def _clean(html):
    return clean.clean_html(html)

@app.post('/new')
@key404
def new_action():
    tally = tallies.new()
    if(request.forms.name): tally.name = _clean(request.forms.name)
    if(request.forms.desc): tally.desc = _clean(request.forms.desc)
    if(request.forms.initial): tally.initial = float(request.forms.initial)
    if(request.forms.unit): tally.unit = _clean(request.forms.unit)
    if(request.forms.inc): tally.buttons = request.forms.getall('inc')
    return redirect('/' + tally.key)

def view_tally_route_websocket_connect(wsock, key=None):
    def key_changed(key=None, value=None):
        wsock.send(json.dumps({'message': 'changed',
                               'key': key,
                               'value': value}))

    pub.subscribe(key_changed, Tally.TALLY_CHANGED_TOPIC.format(key))

    # pub sub is weak reference so send ref of key_changed back
    # to event loop scope to keep it alive.
    return [key_changed]

def view_tally_route_websocket_message(wsock, message, key=None):
    decoded = json.loads(message)
    if('message' in decoded
       and decoded['message'] == 'inc'
       and 'key' in decoded
       and 'inc' in decoded):
        tally = tallies.get(decoded['key'])
        tally.inc(float(decoded['inc']))

# base route for individual tally
key_route = '/<key:re:[' + KEY_SPACE + ']*>'

@app.route(key_route)
@websocket(connect=view_tally_route_websocket_connect,
           message=view_tally_route_websocket_message)
@view('tally')
@key404
def view_tally_route(key=None):
    tally = tallies.get(key)
    return {'key': tally.key,
            'value': tally.value,
            'name': tally.name,
            'desc': tally.desc,
            'initial': tally.initial,
            'unit': tally.unit,
            'buttons': tally.buttons}

@app.post(key_route + '/inc')
@key404
def inc_action(key=None):
    inc = float(request.forms.inc)
    tally = tallies.get(key)
    tally.inc(inc)
    return redirect('/' + tally.key)

@app.route('/static/<filepath:path>')
def static_route(filepath):
    return static_file(filepath, root='{0}/static'.format(os.path.dirname(__file__)))

def main():
    parser = argparse.ArgumentParser(
        description='Tally server (v{0}). Create and share a counter.'.format(version.get_version()))
    parser.add_argument('-a', '--address', default="0.0.0.0",
                        help="the ip address to bind to.",
                        type=str)
    parser.add_argument('-p', '--port', default=8080,
                        help="the port number to bind to.",
                        type=int)
    args = parser.parse_args()

    server = WSGIServer((args.address, args.port), app,
                        handler_class=WebSocketHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
