import random
import string
import math
from pubsub import pub
from datetime import datetime
from time import mktime

class OutOfKeysError(Exception):
    pass

class Tally():

    VALUE_CHANGED_TOPIC = 'value.changed.key{0}'

    def __init__(self, global_key_length=1, global_max_key_length = 5):
        self.key_length = global_key_length
        self.max_key_length = global_max_key_length
        self.tallys = {}

    key_space = 'ABCDEFGHJKLMNPQRSTUVWXY123456789'
    key_bits_per_char = int(math.ceil(math.log(len(key_space), 2)))

    def new_key(self):
        key_exists = True
        tries = 42
        key = ''
        while key_exists and tries > 0:
            dt = datetime.now()
            micros_since_epoch = int((mktime(dt.timetuple()) * 1000000)  + dt.microsecond)
            bits_in_time = int(math.floor(math.log(micros_since_epoch, 2)) + 1)
            chars_in_key = int(math.ceil(bits_in_time / Tally.key_bits_per_char))

            for n in range(chars_in_key):
                mask = int(math.pow(2, Tally.key_bits_per_char)-1) << (n * 5)
                index = (micros_since_epoch & mask) >> (n * 5)
                key = key + Tally.key_space[index]

            key_exists = key in self.tallys
            if key_exists: key = None
            tries = tries - 1

        self.tallys[key] = 0
        return key

    def inc(self, key, inc=1):
        current_tally = self.get(key)
        self.tallys[key] = current_tally + int(inc)
        pub.sendMessage(Tally.VALUE_CHANGED_TOPIC.format(key), key=key, value=self.tallys[key])
        return self.tallys[key]

    def get(self, key):
        return self.tallys[key]
