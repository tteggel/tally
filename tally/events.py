from pubsub import pub
from functools import wraps


_CHANGED_FIELD_TOPIC = 'tally.changed.{0}'
def on_value_changed_all(function):
    pub.subscribe(function, _CHANGED_FIELD_TOPIC.format('value'))

_CHANGED_FIELD_TOPIC_PER_KEY = _CHANGED_FIELD_TOPIC + '.key{1}'
def on_value_changed(function, key):
    pub.subscribe(function, _CHANGED_FIELD_TOPIC_PER_KEY.format('value', key))
def value_changed(tally):
    pub.sendMessage(_CHANGED_FIELD_TOPIC_PER_KEY.format('value', tally.key),
                    tally=tally)

_NEW_TOPIC = 'tally.new'
def on_new_tally(function):
    pub.subscribe(function, _NEW_TOPIC)
def new_tally(tally):
    pub.sendMessage(_NEW_TOPIC, tally=tally)

def publish_changes(field):
    def decorator(f):
        def wrapper(self, *a, **ka):
            topic = _CHANGED_FIELD_TOPIC_PER_KEY.format(field, self.key)
            pub.sendMessage(topic, tally=self)
            f(self, *a, **ka)
        return wraps(f)(wrapper)
    return decorator
