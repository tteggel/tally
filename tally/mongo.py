from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

import events

class Mongo():

    __started = False

    def __init__(self):
        if Mongo.__started:
            return

        try:
            self.connection = MongoClient()
            self.db = self.connection.tally
            self.tallies = self.db.tallies
            self.tally_events = self.db.tally_events
        except ConnectionFailure:
            pass

        events.on_new_tally(self.insert_tally)
        events.on_value_changed_all(self.update_value)

        Mongo.__started = True

    def insert_tally(self, tally=None):
        if self.connection.alive():
            # add the tally to the tally collection
            s = tally._serialise()
            s['_id'] = s['key']
            self.tallies.insert(s)

            # record the event in the tally_events collection
            event = {'timestamp': datetime.now(),
                     'event': 'new',
                     'tally': tally._serialise()}
            self.tally_events.insert(event)

    def update_value(self, tally=None):
        if self.connection.alive():
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

    def __getitem__(self, key):
        d = None
        if self.connection.alive():
            d = self.tallies.find_one({'_id': key})
        return d
