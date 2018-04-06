#!/usr/bin/env python3

class Coin:
    
    def __init__(self, name, rank, cmc_path):
        self.name = name
        self.rank = rank
        self.cmc_path = cmc_path

    def set_data(self, data):
        self.data = data

    def set_cc_data(self, cc_data):
        self.cc_data = cc_data 

    def __str__(self):
        return self.name + ' at ' + self.cmc_path

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

    def to_dict(self, coin_name, coin_rank, cc_data):
        obj = {}
        # These values are the same for all entries on a coin, and definitely
        # shouldn't be duplicated across all objects.
        obj['name'] = coin_name
        obj['rank'] = coin_rank
        if cc_data:
            algorithm, proof_type, sponsored = cc_data
            obj['algorithm'] = algorithm
            obj['proof_type'] = proof_type
            obj['sponsored'] = sponsored
        
        # these fields are per-date
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
