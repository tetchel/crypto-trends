#!/usr/bin/env python3

import sys
from pytrends.request import TrendReq
from datetime import datetime
from mongo import trends_insert, db

pytrends = TrendReq()

if len(sys.argv) > 1 and sys.argv[1] == 'drop':
    db.trends.drop()
    print('Dropped trends collection')
    exit()

keywords = sys.argv[1:]#.lower().split()
keywords = [keyword.strip() for keyword in keywords]
print(keywords)

for kw in keywords:
    print('Getting trends for ' + kw)
    pytrends.build_payload(kw_list=[kw], cat=0, timeframe='today 5-y')  # should calculate time since cmc.start_date
    result = pytrends.interest_over_time()
    #print(result)

    for t in result.itertuples():
        date = t[0].to_pydatetime()
        interest = t[1]
        #print('time {} interest {}'.format(date, interest))
        # The 'schema' for the trends collection is date, keyword, and interest
        trends_insert(kw, date, interest)
        

