import random
import string
import math
from pubsub import pub
from datetime import datetime
from time import mktime
from functools import wraps

KEY_SPACE = 'ABCDEFGHJKLMNPQRSTUVWXY123456789'

class Tally(object):
    CHANGED_FIELD_TOPIC = 'tally.changed.key{0}.{1}'
    CHANGED_TOPIC = 'tally.changed.key{0}'
    NEW_TOPIC = 'tally.new'

    def publish_changes(field):
        def decorator(f):
            def wrapper(self, *a, **ka):
                topic = Tally.CHANGED_FIELD_TOPIC.format(self.key, field)
                pub.sendMessage(topic, tally=self)
                f(self, *a, **ka)
            return wraps(f)(wrapper)
        return decorator


    def __init__(self):
        self._key = self.new_key()
        self._value = 0.0
        self._name = None
        self._desc = None
        self._initial = 0.0
        self._unit = None
        self._buttons = []

    @property
    def initial(self):
        return self._initial

    @initial.setter
    @publish_changes('initial')
    def initial(self, v):
        self._initial = v
        self._value = v

    @property
    def buttons(self):
        return self._buttons

    @buttons.setter
    @publish_changes('buttons')
    def buttons(self, vs):
        self._buttons = [float(v) for v in vs]

    @property
    def name(self):
        return self._name

    @name.setter
    @publish_changes('name')
    def name(self, v):
        self._name = v

    @property
    def desc(self):
        return self._desc

    @desc.setter
    @publish_changes('desc')
    def desc(self, v):
        self._desc = v

    @property
    def unit(self):
        return self._unit

    @unit.setter
    @publish_changes('unit')
    def unit(self, v):
        self._unit = v

    @property
    def value(self):
        return self._value

    @property
    def key(self):
        return self._key

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

    def inc(self, inc=1.0):
        self._value = self._value + float(inc)
        topic = Tally.CHANGED_FIELD_TOPIC.format(self.key, 'value')
        pub.sendMessage(topic, tally=self)
        return self._value

class Tallies():
    def __init__(self):
        self._tallies = {}

    def get(self, key):
        return self._tallies[key]

    def new(self):
        new = Tally()
        self._tallies[new.key] = new
        pub.sendMessage(Tally.NEW_TOPIC, tally=self)
        return new
