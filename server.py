from bottle import Bottle, view, static_file, redirect, abort, request

from tally import Tally

tally = Tally()
app = Bottle()

def key_404(f):
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
@key_404
def new_action():
    key = tally.new_key()
    return redirect('/' + key)

# base route for individual tally
key_route = '/<key:re:[a-z]*>'

@app.route(key_route)
@view('tally')
@key_404
def view_tally_route(key=None):
    value = tally.get(key)
    return {'key': key, 'value': value}

@app.post(key_route + '/inc')
@key_404
def inc_action(key=None):
    inc = int(request.forms.inc)
    tally.inc(key, inc)
    return redirect('/' + key)

@app.route('/static/<filepath:path>')
def static_route(filepath):
    return static_file(filepath, root='./static')

if __name__ == "__main__":
    from gevent.pywsgi import WSGIServer
    from geventwebsocket import WebSocketHandler, WebSocketError
    server = WSGIServer(("0.0.0.0", 8080), app,
                        handler_class=WebSocketHandler)
    server.serve_forever()
