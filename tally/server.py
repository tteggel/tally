import bottle
from bottle import Bottle, view, static_file, redirect, abort, request
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError, WebSocketHandler

from pubsub import pub
import json
import argparse
import os
from functools import wraps
import logging

from tally import Tally
import version

tally = Tally()
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
                    if connect: persist = connect(wsock, *a, **ka)
                except WebSocketError:
                    if(error): error(wsock, *a, **ka)

                while True:
                    try:
                        raw = wsock.receive()
                        if (raw and message):
                            message(wsock, raw, *a, **ka)
                    except WebSocketError:
                        if error: error(wsock, *a, **ka)
                        break
        return wraps(f)(wrapped)
    return decorator

@app.route('/')
@view('index')
def index_route():
    return {}

@app.post('/new')
@key404
def new_action():
    key = tally.new_key()
    return redirect('/' + key)

def view_tally_route_websocket_connect(wsock, key=None):
    def key_changed(key=None, value=None):
        wsock.send(json.dumps({'message': 'changed',
                               'key': key,
                               'value': value}))

    pub.subscribe(key_changed, Tally.VALUE_CHANGED_TOPIC.format(key))

    # nasty hack to keep this function in scope
    # for duration of ws connection
    return [key_changed]

def view_tally_route_websocket_message(wsock, message, key=None):
    decoded = json.loads(message)
    if('message' in decoded
       and decoded['message'] == 'inc'
       and 'key' in decoded
       and 'inc' in decoded):
        tally.inc(key, decoded['inc'])

# base route for individual tally
key_route = '/<key:re:[' + Tally.key_space + ']*>'

@app.route(key_route)
@websocket(connect=view_tally_route_websocket_connect,
           message=view_tally_route_websocket_message)
@view('tally')
@key404
def view_tally_route(key=None):
    value = tally.get(key)
    return {'key': key, 'value': value}

@app.post(key_route + '/inc')
@key404
def inc_action(key=None):
    inc = int(request.forms.inc)
    tally.inc(key, inc)
    return redirect('/' + key)

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
