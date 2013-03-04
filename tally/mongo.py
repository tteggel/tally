from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, AutoReconnect
from bson.objectid import ObjectId
from datetime import datetime

import events
from retry import retry
import config
from config import Bunch

class Mongo(object):

    __started = False

    def __init__(self):
        if Mongo.__started:
            return

        try:
            self.connection = MongoClient(host=config.mongo.host, port=config.mongo.port)
            self.db = self.connection.tally
            self.tallies = self.db.tallies
            self.tally_events = self.db.tally_events
        except ConnectionFailure:
            self.connection = Bunch(alive=lambda: False)

        events.on_new_tally(self.insert_tally)
        events.on_value_changed_all(self.update_value)

        Mongo.__started = True

    def insert_tally(self, tally=None):
        @retry(AutoReconnect, tries=7, delay=1, backoff=2)
        def _retry():
            if not self.connection.alive(): return

            # add the tally to the tally collection
            s = tally._serialise()
            s['_id'] = s['key']
            self.tallies.insert(s)

            # record the event in the tally_events collection
            event = {'timestamp': datetime.now(),
                     'event': 'new',
                     'tally': tally._serialise()}
            self.tally_events.insert(event)

        _retry()

    def update_value(self, tally=None):
        @retry(AutoReconnect, tries=7, delay=1, backoff=2)
        def _retry():
            if not self.connection.alive(): return

            # update the value in the tally collection
            self.tallies.update({'_id': tally.key},
                                {'$set': {'value': tally.value}})

            # record the event in the tally_events collection
            event = {'timestamp': datetime.now(),
                     'event': 'update',
                     'field': 'value',
                     'value': tally.value,
                     'key': tally.key}
            self.tally_events.insert(event)

        _retry()

    def __getitem__(self, key):
        @retry(AutoReconnect, tries=7, delay=1, backoff=2)
        def _retry():
            if not self.connection.alive(): return

            d = None
            d = self.tallies.find_one({'_id': key})
            return d

        return _retry()
