#!/usr/bin/env python3

import pymongo

url = 'mongodb://localhost:27017/'
db = pymongo.MongoClient(url)
if not db:
    print('Failed to connect to DB at ' + url)

