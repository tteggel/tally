import random
import string
import math
from datetime import datetime
from time import mktime

import events
from events import publish_changes
from mongo import Mongo

# Start mongo inserter / updater
mongo = Mongo()

KEY_SPACE = 'ABCDEFGHJKLMNPQRSTUVWXY123456789'

class Tallies(object):
    def __init__(self):
        self._tallies = {}

    def __getitem__(self, key):
        if key in self._tallies:
            return self._tallies[key]
        else:
            d = mongo[key]
            if d:
                t = Tally(ghost=True)
                t._deserialise(d)
                self._tallies[t.key] = t
                return t
            else:
                raise KeyError()

    def __setitem__(self, key, value):
        self._tallies[key] = value

class Tally(object):

    def __init__(self, name=None, desc=None,
                 initial=0.0, unit=None, buttons=[], ghost=False):
        self._value = initial if initial else 0.0
        self._name = name if name else None
        self._desc = desc if desc else None
        self._initial = initial if initial else 0.0
        self._unit = unit if unit else None
        self._buttons = buttons if buttons else []
        if not ghost:
            self._key = self.new_key()
            events.new_tally(self)

    def _serialise(self):
        return {'key': self.key,
                'value': self.value,
                'name': self.name,
                'desc': self.desc,
                'initial': self.initial,
                'unit': self.unit,
                'buttons': self.buttons}

    def _deserialise(self, d):
        self._key = d['key']
        self._value = d['value']
        self._name = d['name']
        self._desc = d['desc']
        self._initial = d['initial']
        self._unit = d['unit']
        self._buttons = d['buttons']

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
        events.value_changed(self)
        return self._value
