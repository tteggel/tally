import bottle

from tally import Tally

tally = Tally()

def key_404(f):
    """
    Make KeyErrors return 404.
    Apply to any route or action that takes a key as parameter.
    """
    def wrapped(*a, **ka):
        try:
            return f(*a, **ka)
        except KeyError:
            return bottle.abort(404, "Key Not Found")
    return wrapped

@bottle.route('/')
@bottle.view('index')
def index_route():
    return {}

@bottle.post('/new')
@key_404
def new_action():
    key = tally.new_key()
    return bottle.redirect('/' + key)

# base route for individual tally
key_route = '/<key:re:[a-z]*>'

@bottle.route(key_route)
@bottle.view('tally')
@key_404
def view_tally_route(key=None):
    value = tally.get(key)
    return {'key': key, 'value': value}

@bottle.post(key_route + '/inc')
@key_404
def inc_action(key=None):
    inc = int(bottle.request.forms.inc)
    tally.inc(key, inc)
    return bottle.redirect('/' + key)

@bottle.route('/static/<filepath:path>')
def static_route(filepath):
    return bottle.static_file(filepath, root='./static')

if __name__ == "__main__":
    app = bottle.default_app()

    from waitress import serve
    serve(app)
