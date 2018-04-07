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
        insert_id = coins_coll.insert_one(day.to_dict(coin.name.lower(), coin.rank, coin.cc_data))


def trends_insert(keyword, date, interest):
    insert_id = db.trends.insert_one({'keyword': keyword, 'date': date, 'interest': interest})

''' 
Example of conditions dictionary:
name="bitcoin, ethereum"
sponsored="false"
proof_method="PoW"
'''
def query(collection, conditions):
   
    start_date = ''
    end_date = ''
    print('conditions:')
    print(conditions)
    clauses = [] 
    for key, accepted_values in conditions.items():
        if key == 'start_date':
            start_date = accepted_values
            continue
        if key == 'end_date':
            end_date = accepted_values
            continue
            
        if len(accepted_values) < 2:
            clauses.append({ key : accepted_values[0] })
        else:
            or_clause = []
            for v in accepted_values:
                or_clause.append({ key : v })

            clauses.append({ '$or': or_clause })

    if len(clauses) < 2:
        selection = clauses[0]
    else:
        selection = { '$and': clauses }


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


