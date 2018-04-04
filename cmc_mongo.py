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

def clear():
    coins_coll.drop()

# Input: Array of CoinData types
def insert(coin):
    print('insert coin ' + coin.name)
    coin_data = coin.data
    for day in coin_data:
        insert_id = coins_coll.insert_one(day.to_dict(coin.name.lower()))

def get(coin, start_date=None, end_date=None):
    selection = { 'name': coin }

    # dates MUST BE datetime objects
    if start_date:
        selection['date'] = { '$gte': start_date }
    if end_date:
        selection['date'] = { '$lte': end_date }

    print('sel ' + str(selection))
    result = coins_coll.find(selection)
    for r in result:
        print(r)

    return result


