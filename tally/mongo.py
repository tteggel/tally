from pymongo import MongoClient
from bson.objectid import ObjectId

import events

class Mongo():

    def __init__(self):
        self.connection = MongoClient()
        self.db = self.connection.tally
        self.tallies = self.db.tallies

        events.on_new_tally(self.insert_tally)
        events.on_value_changed_all(self.update_value)

    def insert_tally(self, tally=None):
        s = tally._serialise()
        s['_id'] = s['key']
        self.tallies.insert(s)

    def update_value(self, tally=None):
        self.tallies.update({'_id': tally.key},
                            {'$set': {'value': tally.value}})

    def __getitem__(self, key):
        d = self.tallies.find_one({'_id': key})
        return d
