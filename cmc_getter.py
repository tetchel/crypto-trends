#!/usr/bin/env python3

class Coin:
    
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def set_data(self, data):
        self.data = data

    def __str__(self):
        return self.name + ' at ' + self.path


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

    print('coin ' + str(coins[len(coins)-1]))

# Now get the historical data for each coin
for coin in coins:
    coin_response = urllib.request.urlopen(base_url + coin.path + historical_data_path + date_str)
    coin_data = coin_response.read()
    coin_soup = BeautifulSoup(coin_data, 'html.parser')

    data_table = coin_soup.find('table')
    print(data_table)

    # coin.set_data()

