#!/usr/bin/env bash

# stupid little script to run all the update operations at once

echo "Beginning update"

echo "Getting CMC data, takes about 2 minutes"
./cmc_getter.py
echo "Getting Trends data, takes about 10 seconds"
./trends_getter.py "cryptocurrency, blockchain, bitcoin, ethereum, ether, ripple, xrp"

echo "Finished updating"
