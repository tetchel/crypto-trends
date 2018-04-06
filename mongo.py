#!/usr/bin/env python3

import pymongo

url = 'mongodb://localhost:27017/'
db = pymongo.MongoClient(url).coins_db
if not db:
    print('Failed to connect to DB at ' + url)
    exit()


def cmc_insert(coin):
    #print('insert coin ' + coin.name)
    coins_coll = db.coins
    for day in coin.data:
        insert_id = coins_coll.insert_one(day.to_dict(coin.name.lower()))


def trends_insert(keyword, date, interest):
    insert_id = db.trends.insert_one({'keyword': keyword, 'date': date, 'interest': interest})


def query(collection, key_name, keys, start_date=None, end_date=None):
    if len(keys) < 2:
        selection = { key_name : keys[0] }
    else:
        or_clause = []
        for key in keys:
            or_clause.append({ key_name : key })

        selection = { '$or': or_clause }

    # dates MUST BE datetime objects
    if start_date:
        if end_date:
            selection['date'] = { '$gte': start_date, '$lte': end_date }
        else:
            selection['date'] = { '$gte': start_date }
    elif end_date:
        selection['date'] = { '$lte': end_date }

    print('selection: ' + str(selection))
    result = collection.find(selection, { '_id': 0 })

    return result


