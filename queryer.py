#!/usr/bin/env python3

import sys
from cmc_mongo import get

coin = sys.argv[1].lower()
start_date = ''
end_date = ''
if len(sys.argv) > 2:
    start_date = sys.argv[2]
    
    if len(sys.argv) > 3:
        end_date = sys.argv[3]

result = get(coin, start_date, end_date)
