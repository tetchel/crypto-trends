#!/usr/bin/env python3

import pymongo
from coin import Coin, CoinData

url = 'mongodb://localhost:27017/'
db = pymongo.MongoClient(url).coins_db
if not db:
    print('Failed to connect to DB at ' + url)
    exit()

coins_coll = db.coins

def clear():
    coins_coll.drop()

# Input: Array of CoinData types
def insert(coin):
    print('insert coin ' + coin.name)
    coin_data = coin.data
    for day in coin_data:
        insert_id = coins_coll.insert_one(day.to_dict(coin.name.lower()))

def get(coins, start_date=None, end_date=None):
    if len(coins) < 2:
        selection = { 'name': coins[0] }
    else:
        or_clause = []
        for coin in coins:
            or_clause.append({ 'name': coin })

        selection = { '$or': or_clause }

    # dates MUST BE datetime objects
    if start_date:
        if end_date:
            selection['date'] = { '$gte': start_date, '$lte': end_date }
        else:
            selection['date'] = { '$gte': start_date }
    elif end_date:
        selection['date'] = { '$lte': end_date }

    print('sel ' + str(selection))
    result = coins_coll.find(selection, { '_id': 0 })
    for r in result:
        print(r)

    return result


