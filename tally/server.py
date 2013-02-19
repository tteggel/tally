import bottle
from bottle import Bottle, view, static_file, redirect, abort, request
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError, WebSocketHandler

from pubsub import pub
import json
import argparse
import os

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
    def wrapped(*a, **ka):
        try:
            return f(*a, **ka)
        except KeyError:
            return abort(404, "Key Not Found")
    return wrapped

@app.route('/')
@view('index')
def index_route():
    return {}

@app.post('/new')
@key404
def new_action():
    key = tally.new_key()
    return redirect('/' + key)

# base route for individual tally
key_route = '/<key:re:[' + Tally.key_space + ']*>'

@app.route(key_route)
@view('tally')
@key404
def view_tally_route(key=None):

    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        # normal HTTP GET
        value = tally.get(key)
        return {'key': key, 'value': value}
    else:
        # websocket request
        def key_changed(key, value):
            wsock.send(json.dumps({'message': 'changed',
                                   'key': key,
                                   'value': value}))
        pub.subscribe(key_changed, Tally.VALUE_CHANGED_TOPIC.format(key))
        while True:
            try:
                raw = wsock.receive()
            except WebSocketError:
                break
            if (raw):
                decoded = json.loads(raw)
                if('message' in decoded
                   and decoded['message'] == 'inc'
                   and 'key' in decoded
                   and 'inc' in decoded):
                    tally.inc(key, decoded['inc'])

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
