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
