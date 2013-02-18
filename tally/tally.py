import random
import string
import math
from pubsub import pub

class OutOfKeysError(Exception):
    pass

class Tally():

    def __init__(self, global_key_length=1, global_max_key_length = 5):
        self.key_length = global_key_length
        self.max_key_length = global_max_key_length
        self.tallys = {}

    def new_key(self):

        def find_key():
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
            key = find_key()
            if key == None:
                self.key_length = self.key_length + 1
        if key == None: raise OutOfKeysError
        self.tallys[key] = 0
        return key

    def inc(self, key, inc=1):
        current_tally = self.get(key)
        self.tallys[key] = current_tally + int(inc)
        pub.sendMessage('key.changed.{0}'.format(key), key=key, value=self.tallys[key])
        return self.tallys[key]

    def get(self, key):
        return self.tallys[key]