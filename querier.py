#!/usr/bin/env python3

import sys
from datetime import datetime
from mongo import query, db

# Get dates from sysargs and return them as a tuple.
# If an arg is not given, returns None in its place
# Index parameters are indices within sys.argv
def prepare_dates(start_date_index=1, end_date_index=2):
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

# For each argument 
def build_conditions(args):
    conditions = {}
    for arg in args:
        split_eq = arg.split('=', 1)
        key = split_eq[0]
        value = split_eq[1]

        if key == "start_date" or key == "end_date":
            date = format_date(value)
            conditions[key] = date
        else:
            split_value = value.lower().split(',')
            split_value = [s.strip() for s in split_value]
            conditions[key] = split_value

    return conditions


def main(args):
    modes = ['cmc', 'trends']

    if len(args) < 2:
        print('You need to specify a mode (one of {}) and at least one keyword such as "bitcoin"'.format(modes))
        print('Examples:')
        print('./querier.py cmc start_date=2017 end_date=2018 name="bitcoin, ethereum"')
        print('./querier.py cmc sponsored=false algorithm=Scrypt')
        print('will return CMC data for bitcoin and ethereum between (inclusively) Jan 1 2017 and Jan 1 2018')
        exit()

    mode = args[0].lower().strip()

    conditions = build_conditions(args[1:])
    
    # Keywords or coin names, passed as a quoted, comma-delimted stringk
    
    print('Gathering {} data for {}'.format(mode, conditions))

    if mode == modes[0]:
        collection = db.coins
    elif mode == modes[1]:
        collection = db.trends
    else:
        print('Invalid mode ' + mode)
        exit()

    result = query(collection, conditions)
    for r in result:
        print(r)


if __name__ == "__main__":
    main(sys.argv[1:])
