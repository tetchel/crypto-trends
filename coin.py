#!/usr/bin/env python3

class Coin:
    
    def __init__(self, name, rank, path):
        self.name = name
        self.rank = rank
        self.path = path

    def set_data(self, data):
        self.data = data

    def __str__(self):
        return self.name + ' at ' + self.path

from datetime import datetime

# Class to contain a single coin data point
class CoinData:
    
    def __init__(self, date, open_, high, low, close, volume, cap):
        self.date = datetime.strptime(date, "%b %d, %Y")
        self.open_ = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.cap = cap

    def to_dict(self, coin_name, coin_rank):
        obj = {}
        obj['name'] = coin_name
        obj['rank'] = coin_rank
        obj['date'] = self.date
        obj['open'] = self.open_
        obj['high'] = self.high
        obj['low'] = self.low
        obj['close'] = self.close
        obj['volume'] = self.volume
        obj['cap'] = self.cap
        return obj
    
    def __str__(self):
        return 'The data on {} is {} {} {} {} {} {}'.format(self.date, self.open_, self.high, self.low, self.close, self.volume, self.cap)
