#!/usr/bin/env python3

from coin import Coin, CoinData
from mongo import cmc_insert, db

# Replace data with 'null' if it's invalid
def normalize_missing(data):
    if len(data) == 0 or data == '-' or data == 'N/A':
        # should log to a file or something
        return 'null'
    else:
        return data

def parse_coin(coin_data_table):
    all_data = [] 
    for row in coin_data_table.find_all('tr'):
        # Skip table headers
        if row.find_all('th'):
            continue

        #print(row)
        tds = row.find_all('td')
        if len(tds) < 7:
            print('ERROR on row: ' + str(row))
            break
            #continue
        
        #print(tds)
        
        raw_data_attr = 'data-format-value'
        # From left to right, the TDs are as follows:
        # date, Open, High, Low, Close, Volume, Market Cap
        date = normalize_missing(tds[0].text.strip())
        open_ = normalize_missing(tds[1][raw_data_attr].strip())
        high = normalize_missing(tds[2][raw_data_attr].strip())
        low = normalize_missing(tds[3][raw_data_attr].strip())
        close = normalize_missing(tds[4][raw_data_attr].strip())
        volume = normalize_missing(tds[5][raw_data_attr].strip())
        cap = normalize_missing(tds[6][raw_data_attr].strip())

        all_data.append(CoinData(date, open_, high, low, close, volume, cap))

    return all_data

def start_date():
    return '20130428'

import urllib.request
import datetime
import sys
from bs4 import BeautifulSoup
from cc_getter import get_cc_data

base_url = 'https://coinmarketcap.com'
coins_path = '/coins'
historical_data_path = 'historical-data/'

# This is the date parameter added to historical data
# There doesn't seem to be a way to get today's date from the page
# so we have to generate that ourselves
date_str = '?start=' + start_date() + '&end='

now = datetime.datetime.now()
now_str = now.strftime('%Y%m%d')
date_str = date_str + now_str

db.coins.drop()

# First, get /coins/
coins_response = urllib.request.urlopen(base_url + coins_path)
coins_data = coins_response.read()
coins_soup = BeautifulSoup(coins_data, 'html.parser')

coins = []
rank = 1

# Get all <a class="currency-name-container"
# The text of the link is the currency name
# The actual href goes to the currency's page
for link in coins_soup.find_all('a', { 'class' : 'currency-name-container' }):
    coin_name = link.text.strip()
    # stupid hardcoded fix for Experience Points, the only one in the top 100 with a name too long
    if coin_name == 'Experience Po...':
        coin_name = 'Experience Points'

    coin = Coin(coin_name, rank, link['href'])

    cc_data = get_cc_data(coin_name)
    # note cc_data could be None
    coin.set_cc_data(cc_data)

    # Grab CryptoCompare data for this coin
    coins.append(coin) 
    rank = rank + 1

    #print('coin ' + str(coins[len(coins)-1]))

# if CL args specified coins, only get those coins, else get all
if len(sys.argv) > 1:
    for (index, arg) in enumerate(sys.argv):
        sys.argv[index] = arg.lower()

    coins = [coin for coin in coins if coin.name.lower() in sys.argv]

for coin in coins:
    print('Getting CoinMarketCap data for coin ' + coin.name)
    # Now get the historical data for each coin
    coin_response = urllib.request.urlopen(base_url + coin.cmc_path + historical_data_path + date_str)
    coin_data = coin_response.read()
    coin_soup = BeautifulSoup(coin_data, 'html.parser')

    data_table = coin_soup.find('table')
    #print('here is the data for the coin ' + coin.name)
    #print(data_table)
    data = parse_coin(data_table)
    coin.set_data(data)
    cmc_insert(coin)
    #break
    

