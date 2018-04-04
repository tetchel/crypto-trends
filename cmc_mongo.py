#!/usr/bin/env python3

import pymongo
from coin import Coin, CoinData

url = 'mongodb://localhost:27017/'
db = pymongo.MongoClient(url).coins_db
if not db:
    print('Failed to connect to DB at ' + url)
    exit()

coins_coll = db.coins
# Obviously this is not the best way to handle this, but it is certainly the easiest.
coins_coll.drop()

# Input: Array of CoinData types
def insert(coin):
    print('insert coin ' + coin.name)
    coin_data = coin.data
    for day in coin_data:
        insert_id = coins_coll.insert_one(day.to_dict(coin.name))
