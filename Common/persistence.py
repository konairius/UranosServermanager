from Common.models import Serializable

__author__ = 'konsti'

import pymongo

dbname = 'servermanger'
db = pymongo.MongoClient()[dbname]


def save(thing: Serializable):
    serial = thing.serial()
    collection = db[thing.base_name()]
    collection.posts.insert(serial)

