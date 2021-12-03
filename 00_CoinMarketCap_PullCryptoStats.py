# -*- coding: utf-8 -*-

'''This code pulls all coins from Conmarketcap.com
It stores it in a pandas dataframe'''

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import collections


def coinmarketcap_coins(n):
    '''This function pulls all the cryptocurrencies and its related statistics
    from the table that you see in the first page of coinmarketcap.com.
    This doesnt pull the history of a coin
    Input number of pages worth of cryptocurrency to pull'''

    df_coindata = pd.DataFrame()  # create an empty dataframe to add coins

    # Loop through the number of coinmarketcap pages
    # Use n + 1 for the last page as Python range (1, n) is actually 1 to (n-1)
    for pages in range(1, n + 1):

        # Request the coin informations and make it pretty with beautifulsoup
        cmc = requests.get('https://coinmarketcap.com/?page=' + str(pages))
        soup = BeautifulSoup(cmc.content, 'html.parser')

        # Find where the cryptocurrency data resides in html
        # This is is json format with script id __NEXT_DATA__
        data = soup.find('script', id="__NEXT_DATA__", type="application/json")

        # Load the contents of json data
        coin_data = json.loads(data.contents[0])

        # Find where the coin data actually is
        # Here you find keyattributes/colnames in the dictionary
        # Each Crypto stats is in rows with the order following keyattributes
        listings = coin_data['props']['initialState']['cryptocurrency']
        ['listingLatest']['data']

        # Loop through it to match the keysAttribute to data
        # Assign it and create a dicitonary for each coin
        # Is there a better way of doing it?
        # IDK Just my first few weeks of dedicated python coding
        coindata_cmb = {"data": []}
        coindata_cmb = collections.defaultdict(list)
        for k in range(1, len(listings)):
            coins = {}
            coins = collections.defaultdict(list)
            coindata_cmb["data"].append(coins)
            for i in range(len(listings[0]['keysArr'])):
                coins[listings[0]['keysArr'][i]] = listings[k][i]

        # Combine all the coins data
        # You have each key as keyattributes/colnames and values for each coin
        temp_comb_coindata = collections.defaultdict(list)
        for d in coindata_cmb['data']:
            for k, v in d.items():
                temp_comb_coindata[k].append(v)

        # Convert the coins into a pandas dataframe
        df_coins = pd.DataFrame.from_dict(temp_comb_coindata)

        # Concatenate all the data together to have one big dataset
        df_coindata = pd.concat([df_coindata, df_coins], axis=0, sort=False,
                                ignore_index=True)


# =============================================================================
#     There is way too many variables
#     Not all of them is useful but keep them all
#     Reorder some variables that helps to figure out what you are looking at
#     Risk - Errros if coinmarketcap changed the names of these variables
#     But should be relatively easy to fix
# =============================================================================
    var_first = ["rank", "cmcRank", "id", "name", "symbol", "slug", "isActive",
                 "isAudited", "dateAdded", "lastUpdated", "quote.USD.price",
                 "ath", "atl", "high24h", "low24h", "circulatingSupply",
                 "maxSupply", "totalSupply", "quote.USD.marketCap",
                 "quote.USD.marketCapByTotalSupply",
                 "quote.USD.fullyDilluttedMarketCap"]
    var_order = var_first + list(set(list(df_coindata)) - set(var_first))
    # Final dataframe to return
    df_coindata = df_coindata[var_order]
    return(df_coindata)


df_allcoins = coinmarketcap_coins(79)
