import bottle
import random
import string
import math


class Tally():

    class OutOfKeysError(Exception):
        """What happens when we run out of keys?"""
        pass

    def __init__(self, global_static_file_root='./static',
                 global_key_length=1, global_max_key_tries=50, global_max_key_length = 5):
        self.static_file_root = global_static_file_root
        self.key_length = global_key_length
        self.max_key_tries = global_max_key_tries
        self.max_key_length = global_max_key_length
        self.tallys = {}

    @bottle.route('/')
    @bottle.view('index')
    def index(self):
        return {}

    def gen_key(self):
        key_exists = True
        tries = 0
        key = None
        while key_exists and tries < (math.pow(26, self.key_length)*5):
            key = ''.join(random.choice(string.ascii_lowercase)
                          for x in range(self.key_length))
            key_exists = key in self.tallys
            if key_exists: key = None
            tries = tries + 1
        return key

    def new_key(self):
        key = None
        while key == None and self.key_length <= self.max_key_length:
            key = self.gen_key()
            if key == None:
                self.key_length = self.key_length + 1
        if key == None: raise self.OutOfKeysError()
        self.tallys[key] = key
        return key

    @bottle.post('/new')
    def new(self):
        key = new_key()
        return bottle.redirect('/' + key)

    @bottle.get('/<key:re:[a-z]*>')
    @bottle.view('tally')
    def view_tally(self, key=None):
        if key==None or not key in self.tallys: return bottle.abort(404)
        return {'key': key, 'value': self.tallys[key]}

    @bottle.post('/<key:re:[a-z]*>/inc')
    def inc(self, key=None):
        if key==None or not key in self.tallys: return bottle.abort(404)
        inc = bottle.request.forms.inc
        self.tallys[key] = self.tallys[key] + int(inc)
        return bottle.redirect('/' + key)

    @bottle.route('/static/<filepath:path>')
    def static(self, filepath):
        return bottle.static_file(filepath, root=self.static_file_root)

if __name__ == "__main__":
    bottle.run()
