from pymongo import MongoClient
from bson.objectid import ObjectId

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
        except ConnectionFailure:
            pass

        events.on_new_tally(self.insert_tally)
        events.on_value_changed_all(self.update_value)

        Mongo.__started = True

    def insert_tally(self, tally=None):
        if self.connection.alive():
            s = tally._serialise()
            s['_id'] = s['key']
            self.tallies.insert(s)

    def update_value(self, tally=None):
        if self.connection.alive():
            self.tallies.update({'_id': tally.key},
                                {'$set': {'value': tally.value}})

    def __getitem__(self, key):
        d = None
        if self.connection.alive():
            d = self.tallies.find_one({'_id': key})
        return d
