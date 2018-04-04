#!/usr/bin/env python3

import pymongo
from coin import Coin, CoinData

url = 'mongodb://localhost:27017/'
db = pymongo.MongoClient(url)
if not db:
    print('Failed to connect to DB at ' + url)

# Input: Array of CoinData types
def insert(coin):
    print('insert coin ' + coin.name)
    coin_data = coin.data
    for day in coin_data:
        print(day)
