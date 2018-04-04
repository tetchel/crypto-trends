#!/usr/bin/env python3

class Coin:
    
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def set_data(self, data):
        self.data = data

    def __str__(self):
        return self.name + ' at ' + self.path

# Class to contain a single coin data point
class CoinData:
    
    def __init__(self, date, open_, high, low, close, volume, cap):
        self.date = date
        self.open_ = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.cap = cap
    
    def __str__(self):
        return 'The data on {} is {} {} {} {} {} {}'.format(self.date, self.open_, self.high, self.low, self.close, self.volume, self.cap)

# Replace data with 'null' if it's invalid
def normalize(data):
    if len(data) == 0 or data == '-':
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
        date = normalize(tds[0].text.strip())
        open_ = normalize(tds[1][raw_data_attr].strip())
        high = normalize(tds[2][raw_data_attr].strip())
        low = normalize(tds[3][raw_data_attr].strip())
        close = normalize(tds[4][raw_data_attr].strip())
        volume = normalize(tds[5][raw_data_attr].strip())
        cap = normalize(tds[6][raw_data_attr].strip())

        all_data.append(CoinData(date, open_, high, low, close, volume, cap))

    return all_data        

import urllib.request
import datetime
from bs4 import BeautifulSoup

base_url = 'https://coinmarketcap.com'
coins_path = '/coins'
historical_data_path = 'historical-data/'

# This is the date parameter added to historical data
# There doesn't seem to be a way to get today's date from the page
# so we have to generate that ourselves
date_str = '?start=20130428&end='

now = datetime.datetime.now()
now_str = now.strftime('%Y%m%d')
date_str = date_str + now_str



# First, get /coins/
coins_response = urllib.request.urlopen(base_url + coins_path)
coins_data = coins_response.read()
coins_soup = BeautifulSoup(coins_data, 'html.parser')

coins = []

# Get all <a class="currency-name-container"
# The text of the link is the currency name
# The actual href goes to the currency's page
for link in coins_soup.find_all('a', { 'class' : 'currency-name-container' }):
    coins.append( Coin(link.text.strip(), link['href']) )

    #print('coin ' + str(coins[len(coins)-1]))

# Now get the historical data for each coin
for coin in coins:
    coin_response = urllib.request.urlopen(base_url + coin.path + historical_data_path + date_str)
    coin_data = coin_response.read()
    coin_soup = BeautifulSoup(coin_data, 'html.parser')

    data_table = coin_soup.find('table')
    #print('here is the data for the coin ' + coin.name)
    #print(data_table)
    data = parse_coin(data_table)
    coin.set_data(data)

