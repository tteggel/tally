import random
import string
import math
from pubsub import pub
from datetime import datetime
from time import mktime

KEY_SPACE = 'ABCDEFGHJKLMNPQRSTUVWXY123456789'


class Tally():
    TALLY_CHANGED_TOPIC = 'value.changed.key{0}'

    def __init__(self):
        self.key = self.new_key()
        self.value = 0
        self.name = None

    def new_key(self):
        key_exists = True
        tries = 42
        key = ''
        key_bits_per_char = int(math.ceil(math.log(len(KEY_SPACE), 2)))

        dt = datetime.now()
        micros_since_epoch = int((mktime(dt.timetuple()) * 1000000)  + dt.microsecond)
        bits_in_time = int(math.floor(math.log(micros_since_epoch, 2)) + 1)
        chars_in_key = int(math.ceil(bits_in_time / key_bits_per_char))

        for n in range(chars_in_key):
            mask = int(math.pow(2, key_bits_per_char)-1) << (n * 5)
            index = (micros_since_epoch & mask) >> (n * 5)
            key = key + KEY_SPACE[index]

        return key

    def inc(self, inc=1):
        self.value = self.value + int(inc)
        pub.sendMessage(Tally.TALLY_CHANGED_TOPIC.format(self.key), key=self.key, value=self.value)
        return self.value

class Tallies():
    def __init__(self):
        self._tallies = {}

    def get(self, key):
        return self._tallies[key]

    def new(self):
        new = Tally()
        self._tallies[new.key] = new
        return new
