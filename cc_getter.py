
import sys
import subprocess
import json

# It's stupid to call an external script and load the output file like this, but I have it working in sh, so why rewrite it in python?

subprocess.call(['./cryptocompare.sh'])

with open('cryptocompare.json', 'r') as cc_json:
    data = json.load(cc_json)['Data']

def normalize(s):
    if s == 'n/a':
        return 'null'

    return s.lower()

# Returns (algorithm, ProofType, Sponsored) for the given coin
def get_cc_data(coin_name):
    for coin in data:
        if coin_name.lower() in data[coin]['CoinName'].lower():
            return (normalize(data[coin]['Algorithm']), normalize(data[coin]['ProofType']), normalize(str(data[coin]['Sponsored'])))

    print('Could not get CryptoCompare data for coin: ' + coin_name)
    return None
