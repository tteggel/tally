import bottle
import random
import string
import math

def route(app):
    # index and static
    bottle.route('/')(app.index_route)
    bottle.route()(app.static_route)


    # actions

    # views
    bottle.route(key_route)(app.view_tally_route)


class Tally():

    class OutOfKeysError(Exception):
        """What happens when we run out of keys?"""
        pass

    def __init__(self, global_key_length=1, global_max_key_length = 5):
        self.key_length = global_key_length
        self.max_key_length = global_max_key_length
        self.tallys = {}

    def new_key(self):

        def gen_key():
            key_exists = True
            tries = 0
            key = None
            while key_exists and tries < (math.pow(26, self.key_length)*10):
                key = ''.join(random.choice(string.ascii_lowercase)
                              for x in range(self.key_length))
                key_exists = key in self.tallys
                if key_exists: key = None
                tries = tries + 1
            return key

        key = None
        while key == None and self.key_length <= self.max_key_length:
            key = gen_key()
            if key == None:
                self.key_length = self.key_length + 1
        if key == None: raise self.OutOfKeysError()
        self.tallys[key] = 0
        return key

    def inc(self, key, amount=1):
        current_tally = self.get(key)
        self.tallys[key] = current_tally + amount
        return self.tallys[key]

    def get(self, key):
        if key not in self.tallys: raise KeyError
        return self.tallys[key]

tally = Tally()

@bottle.route('/')
@bottle.view('index')
def index_route():
    return {}

@bottle.post('/new')
def new_action():
    key = tally.new_key()
    return bottle.redirect('/' + key)

# base route for individual tally
key_route = '/<key:re:[a-z]*>'

@bottle.route(key_route)
@bottle.view('tally')
def view_tally_route(key=None):
    try:
        value = tally.get(key)
        return {'key': key, 'value': value}
    except KeyError:
        return bottle.abort(404)

@bottle.post(key_route + '/inc')
def inc_action(key=None):
    try:
        inc = int(bottle.request.forms.inc)
        tally.inc(key, inc)
        return bottle.redirect('/' + key)
    except KeyError:
        return bottle.abort(404)

@bottle.route('/static/<filepath:path>')
def static_route(filepath):
    return bottle.static_file(filepath, root='./static')

if __name__ == "__main__":
    app = bottle.default_app()

    from waitress import serve
    serve(app)
