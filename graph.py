#!/usr/bin/env python3
import matplotlib as mpl
import matplotlib.patches as mpatches
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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
            split_value = value.lower().split()
            split_value = [s.strip() for s in split_value]
            conditions[key] = split_value

    return conditions


def main(args):
    modes = ['cmc', 'trends']

    queryBitcoinAllTime = "cmc name=bitcoin"
    queryEthereumAllTime = "cmc name=ethereum"
    queryEtherAllTime = "cmc name=ether"
    #queryXrpAllTime = "cmc name=xrp" #works but retunrs nothing
    queryBitcoinApril =  "cmc start_date=2017-04 end_date=2018-04 name=bitcoin" 
    queryBitcoinNovFeb =  "cmc start_date=2017-11 end_date=2018-02 name=bitcoin" 
    queryBlockchainTrends = "trends keyword=blockchain"
    queryBitcoinTrends = "trends keyword=bitcoin"
    queryEtherTrends = "trends keyword=ether"
    queryEthereumTrends = "trends keyword=ethereum"
    queryRippleTrends = "trends keyword=ripple"
    queryXrpTrends = "trends keyword=xrp"

    argumentList = queryBitcoinAllTime.split(" ", 3)

    mode = argumentList[0].lower().strip()
    conditions = build_conditions(argumentList[1:])
   
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
    fig = plt.figure()
    coin1List = []
    coin2List = []
    coList2 = []
    coList1 = []
    coin1 = result[0]['name'] 
    coin2 = ''
    for r in result:
        if r['name'] == coin1:
            coin1List.append(r)
        else:
            coin2 = r['name'] 
            coin2List.append(r)
    ax = fig.add_subplot(111)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    blue_patch = mpatches.Patch(color='blue', label=coin1)
    plt.legend(handles=[blue_patch])
    for c in coin1List:
        ax.scatter(c['date'],float(c['close']),color='blue')
        coList1.append(c['close'])
    for index, label in enumerate(ax.yaxis.get_ticklabels()):
        if index % 100 != 0:
            label.set_visible(False)
    x = np.array(coList1)
    x2 = np.array(coList2)
    y = x.astype(np.float)
    y2 = x.astype(np.float)
    ax.set_title('Bitcoin All Time')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    fig.savefig('bitcoinAllTime.png')

    
    argumentList = queryBitcoinApril.split(" ", 3)
    mode = argumentList[0].lower().strip()
    conditions = build_conditions(argumentList[1:])
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
    fig = plt.figure()
    coin1List = []
    coin2List = []
    coList2 = []
    coList1 = []
    coin1 = result[0]['name'] 
    coin2 = ''
    for r in result:
        if r['name'] == coin1:
            coin1List.append(r)
        else:
            coin2 = r['name'] 
            coin2List.append(r)
    ax = fig.add_subplot(111)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    blue_patch = mpatches.Patch(color='blue', label=coin1)
    plt.legend(handles=[blue_patch])
    for c in coin1List:
        ax.scatter(c['date'],float(c['close']),color='blue')
        coList1.append(c['close'])
    x = np.array(coList1)
    x2 = np.array(coList2)
    y = x.astype(np.float)
    y2 = x.astype(np.float)
    ax.set_title('Bitcoin April 2017 to April 2018 ')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    fig.savefig('bitcoinApril.png')

    argumentList = queryBitcoinNovFeb.split(" ", 3)
    mode = argumentList[0].lower().strip()
    conditions = build_conditions(argumentList[1:])
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
    fig = plt.figure()
    coin1List = []
    coin2List = []
    coList2 = []
    coList1 = []
    coin1 = result[0]['name'] 
    coin2 = ''
    for r in result:
        if r['name'] == coin1:
            coin1List.append(r)
        else:
            coin2 = r['name'] 
            coin2List.append(r)
    ax = fig.add_subplot(111)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    blue_patch = mpatches.Patch(color='blue', label=coin1)
    plt.legend(handles=[blue_patch])
    for c in coin1List:
        ax.scatter(c['date'],float(c['close']),color='blue')
        coList1.append(c['close'])
    x = np.array(coList1)
    x2 = np.array(coList2)
    y = x.astype(np.float)
    y2 = x.astype(np.float)
    ax.set_title('Bitcoin November 2017 to February 2018')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    fig.savefig('bitcoinNovFeb.png')


    argumentList = queryBitcoinAllTime.split(" ", 3)
    argumentList2 = queryBlockchainTrends.split(" ", 3)
    mode = argumentList[0].lower().strip()
    conditions = build_conditions(argumentList[1:])
    mode2 = argumentList2[0].lower().strip()
    conditions2 = build_conditions(argumentList2[1:])
    # Keywords or coin names, passed as a quoted, comma-delimted stringk
    print('Gathering {} data for {}'.format(mode, conditions))
    if mode == modes[0]:
        collection = db.coins
    elif mode == modes[1]:
        collection = db.trends
    else:
        print('Invalid mode ' + mode)
        exit()
    if mode2 == modes[0]:
        collection2 = db.coins
    elif mode2 == modes[1]:
        collection2 = db.trends
    else:
        print('Invalid mode ' + mode2)
        exit()
    result = query(collection, conditions)
    result2 = query(collection2, conditions2)
    fig = plt.figure()
    coin1List = []
    coin2List = []
    coList2 = []
    coList1 = []
    coin1 = result[0]['name'] 
    coin2 = ''
    for r in result:
        coin1List.append(r)
    for r in result2:
        coin2List.append(r)
    ax = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Interest')
    blue_patch = mpatches.Patch(color='blue', label="Bitcoin")
    red_patch = mpatches.Patch(color='red', label="Blockchain Trends")
    plt.legend(handles=[red_patch, blue_patch])
    for c in coin1List:
        ax.scatter(c['date'],float(c['close']),color='blue')
    for c2 in coin2List:
        ax2.scatter(c2['date'],int(c2['interest']),color='red')    
    x = np.array(coList1)
    x2 = np.array(coList2)
    y = x.astype(np.float)
    y2 = x.astype(np.float)
    ax.set_title('Bitcoin Price and Blockchain trends')
    plt.show()
    fig.savefig('bitcoinVSblockchain.png')

    argumentList = queryBitcoinAllTime.split(" ", 3)
    argumentList2 = queryBitcoinTrends.split(" ", 3)
    mode = argumentList[0].lower().strip()
    conditions = build_conditions(argumentList[1:])
    mode2 = argumentList2[0].lower().strip()
    conditions2 = build_conditions(argumentList2[1:])
    # Keywords or coin names, passed as a quoted, comma-delimted stringk
    print('Gathering {} data for {}'.format(mode, conditions))
    if mode == modes[0]:
        collection = db.coins
    elif mode == modes[1]:
        collection = db.trends
    else:
        print('Invalid mode ' + mode)
        exit()
    if mode2 == modes[0]:
        collection2 = db.coins
    elif mode2 == modes[1]:
        collection2 = db.trends
    else:
        print('Invalid mode ' + mode2)
        exit()
    result = query(collection, conditions)
    result2 = query(collection2, conditions2)
    fig = plt.figure()
    coin1List = []
    coin2List = []
    coList2 = []
    coList1 = []
    coin1 = result[0]['name'] 
    coin2 = ''
    for r in result:
        coin1List.append(r)
    for r in result2:
        coin2List.append(r)
    ax = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Interest')
    blue_patch = mpatches.Patch(color='blue', label="Bitcoin")
    red_patch = mpatches.Patch(color='red', label="Bitcoin Trends")
    plt.legend(handles=[red_patch, blue_patch])
    for c in coin1List:
        ax.scatter(c['date'],float(c['close']),color='blue')
    for c2 in coin2List:
        ax2.scatter(c2['date'],int(c2['interest']),color='red')    
    x = np.array(coList1)
    x2 = np.array(coList2)
    y = x.astype(np.float)
    y2 = x.astype(np.float)
    ax.set_title('Bitcoin price and Bitcoin trends')
    plt.show()
    fig.savefig('bitcoinVSbitcoin.png')

    argumentList = queryEthereumAllTime.split(" ", 3)
    argumentList2 = queryEthereumTrends.split(" ", 3)
    mode = argumentList[0].lower().strip()
    conditions = build_conditions(argumentList[1:])
    mode2 = argumentList2[0].lower().strip()
    conditions2 = build_conditions(argumentList2[1:])
    # Keywords or coin names, passed as a quoted, comma-delimted stringk
    print('Gathering {} data for {}'.format(mode, conditions))
    if mode == modes[0]:
        collection = db.coins
    elif mode == modes[1]:
        collection = db.trends
    else:
        print('Invalid mode ' + mode)
        exit()
    if mode2 == modes[0]:
        collection2 = db.coins
    elif mode2 == modes[1]:
        collection2 = db.trends
    else:
        print('Invalid mode ' + mode2)
        exit()
    result = query(collection, conditions)
    result2 = query(collection2, conditions2)
    fig = plt.figure()
    coin1List = []
    coin2List = []
    coList2 = []
    coList1 = []
    coin1 = result[0]['name'] 
    coin2 = ''
    for r in result:
        coin1List.append(r)
    for r in result2:
        coin2List.append(r)
    ax = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Interest')
    blue_patch = mpatches.Patch(color='blue', label="Ethereum")
    red_patch = mpatches.Patch(color='red', label="Ethereum Trends")
    plt.legend(handles=[red_patch, blue_patch])
    for c in coin1List:
        ax.scatter(c['date'],float(c['close']),color='blue')
    for c2 in coin2List:
        ax2.scatter(c2['date'],int(c2['interest']),color='red')    
    x = np.array(coList1)
    x2 = np.array(coList2)
    y = x.astype(np.float)
    y2 = x.astype(np.float)
    ax.set_title('Ethereum price and Ethereum trends')
    plt.show()
    fig.savefig('ethereumVSethereum.png')

    argumentList = queryEthereumAllTime.split(" ", 3)
    argumentList2 = queryEtherTrends.split(" ", 3)
    mode = argumentList[0].lower().strip()
    conditions = build_conditions(argumentList[1:])
    mode2 = argumentList2[0].lower().strip()
    conditions2 = build_conditions(argumentList2[1:])
    # Keywords or coin names, passed as a quoted, comma-delimted stringk
    print('Gathering {} data for {}'.format(mode, conditions))
    if mode == modes[0]:
        collection = db.coins
    elif mode == modes[1]:
        collection = db.trends
    else:
        print('Invalid mode ' + mode)
        exit()
    if mode2 == modes[0]:
        collection2 = db.coins
    elif mode2 == modes[1]:
        collection2 = db.trends
    else:
        print('Invalid mode ' + mode2)
        exit()
    result = query(collection, conditions)
    result2 = query(collection2, conditions2)
    fig = plt.figure()
    coin1List = []
    coin2List = []
    coList2 = []
    coList1 = []
    coin1 = result[0]['name'] 
    coin2 = ''
    for r in result:
        coin1List.append(r)
    for r in result2:
        coin2List.append(r)
    ax = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Interest')
    blue_patch = mpatches.Patch(color='blue', label="Ethereum")
    red_patch = mpatches.Patch(color='red', label="Ether Trends")
    plt.legend(handles=[red_patch, blue_patch])
    for c in coin1List:
        ax.scatter(c['date'],float(c['close']),color='blue')
    for c2 in coin2List:
        ax2.scatter(c2['date'],int(c2['interest']),color='red')    
    x = np.array(coList1)
    x2 = np.array(coList2)
    y = x.astype(np.float)
    y2 = x.astype(np.float)
    ax.set_title('Ethereum price and Ether trends')
    plt.show()
    fig.savefig('ethereumVSether.png')

    argumentList = queryBitcoinAllTime.split(" ", 3)
    argumentList2 = queryEtherTrends.split(" ", 3)
    mode = argumentList[0].lower().strip()
    conditions = build_conditions(argumentList[1:])
    mode2 = argumentList2[0].lower().strip()
    conditions2 = build_conditions(argumentList2[1:])
    # Keywords or coin names, passed as a quoted, comma-delimted stringk
    print('Gathering {} data for {}'.format(mode, conditions))
    if mode == modes[0]:
        collection = db.coins
    elif mode == modes[1]:
        collection = db.trends
    else:
        print('Invalid mode ' + mode)
        exit()
    if mode2 == modes[0]:
        collection2 = db.coins
    elif mode2 == modes[1]:
        collection2 = db.trends
    else:
        print('Invalid mode ' + mode2)
        exit()
    result = query(collection, conditions)
    result2 = query(collection2, conditions2)
    fig = plt.figure()
    coin1List = []
    coin2List = []
    coList2 = []
    coList1 = []
    coin1 = result[0]['name'] 
    coin2 = ''
    for r in result:
        coin1List.append(r)
    for r in result2:
        coin2List.append(r)
    ax = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Interest')
    blue_patch = mpatches.Patch(color='blue', label="Bitcoin")
    red_patch = mpatches.Patch(color='red', label="Ether Trends")
    plt.legend(handles=[red_patch, blue_patch])
    for c in coin1List:
        ax.scatter(c['date'],float(c['close']),color='blue')
    for c2 in coin2List:
        ax2.scatter(c2['date'],int(c2['interest']),color='red')    
    x = np.array(coList1)
    x2 = np.array(coList2)
    y = x.astype(np.float)
    y2 = x.astype(np.float)
    ax.set_title('Bitcoin price and Ether trends')
    plt.show()
    fig.savefig('bitcoinVSether.png')







if __name__ == "__main__":
    main(sys.argv[1:])

