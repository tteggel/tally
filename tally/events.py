from pubsub import pub
from functools import wraps

_CHANGED_FIELD_TOPIC = 'tally.changed.key{0}.{1}'
def on_value_changed(function, key):
    pub.subscribe(function, _CHANGED_FIELD_TOPIC.format(key, 'value'))
def value_changed(tally):
    pub.sendMessage(_CHANGED_FIELD_TOPIC.format(tally.key, 'value'),
                    tally=tally)

_NEW_TOPIC = 'tally.new'
def on_new_tally(function):
    pub.subscribe(function, _NEW_TOPIC)
def new_tally(tally):
    pub.sendMessage(_NEW_TOPIC, tally=tally)

def publish_changes(field):
    def decorator(f):
        def wrapper(self, *a, **ka):
            topic = _CHANGED_FIELD_TOPIC.format(self.key, field)
            pub.sendMessage(topic, tally=self)
            f(self, *a, **ka)
        return wraps(f)(wrapper)
    return decorator
