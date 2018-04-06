#!/usr/bin/env python3

import sys
from datetime import datetime
from mongo import query, db

# Get dates from sysargs and return them as a tuple.
# If an arg is not given, returns None in its place
# Index parameters are indices within sys.argv
def prepare_dates(start_date_index=3, end_date_index=4):
    start_date = ''
    end_date = ''
    if len(sys.argv) > start_date_index:
        start_date = sys.argv[start_date_index]
        
        if len(sys.argv) > end_date_index:
            end_date = sys.argv[end_date_index]
            
    start_date_formatted = '' 
    end_date_formatted = ''
    if start_date:
        start_date_formatted = format_date(start_date)

    if end_date:
        end_date_formatted = format_date(end_date)

    if start_date and end_date and start_date_formatted > end_date_formatted:
        print('Start date cannot be before end date')
        exit()

    return start_date_formatted, end_date_formatted

date_formats = [ '%Y-%m-%d', '%Y-%m', '%Y' ]
def report_malformed_date(date):
    print('Could not parse date: "' + date + '"')
    print('Use the format YYYY-MM-DD, YYYY-MM, or YYYY')

def format_date(date_str):
    formatted = ''
    for df in date_formats:
        try:
            return datetime.strptime(date_str, df)
        except Exception as e:
            #print(e)
            pass

    report_malformed_date(date_str)
    return ''


def main(args):
    modes = ['cmc', 'trends']

    if len(args) < 2:
        print('You need to specify a mode (one of {}) and at least one keyword such as "bitcoin"'.format(modes))
        print('Example:')
        print('./querier.py cmc "bitcoin, ethereum" 2017 2018')
        print('will return CMC data for bitcoin and ethereum between (inclusively) Jan 1 2017 and Jan 1 2018')
        exit()

    mode = args[0].lower().strip()
    
    # Keywords or coin names, passed as a quoted, comma-delimted string
    keywords = args[1].lower().split(',')
    keywords = [keyword.strip() for keyword in keywords]
    
    start_date, end_date = prepare_dates()

    print('Gathering {} data for {} between {} and {}'.format(mode, keywords, start_date, end_date))

    if mode == modes[0]:
        collection = db.coins
        key_name = 'name'
    elif mode == modes[1]:
        collection = db.trends
        key_name = 'keyword'
    else:
        print('Invalid mode ' + mode)

    result = query(collection, key_name, keywords, start_date, end_date)
    for r in result:
        print(r)


if __name__ == "__main__":
    main(sys.argv[1:])
