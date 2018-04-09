#!/usr/bin/env bash

# shortcut script to run all the update operations at once

echo "Beginning update"

echo "Getting CMC data, takes about 2 minutes"
./cmc_getter.py

./trends_getter.py drop
echo "Getting Trends data, takes about 1 second per keyword"
./trends_getter.py cryptocurrency blockchain bitcoin ethereum ether ripple xrp "smart contracts" doge
echo "Finished updating"
