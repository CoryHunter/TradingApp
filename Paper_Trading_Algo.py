# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 19:21:18 2020

@author: coryr
"""
import alpaca_trade_api as tradeapi
import yfinance as yf
import pandas as pd
import time
import matplotlib.pyplot as plt
import bs4 as bs
import pickle
import requests
from time import sleep
from yahoo_finance import Share
import time
from yahoo_fin import stock_info as si

api_key_general = 'PK8BF9YOI8F999R3EYCV'
api_key_secret = 'pWy8ZtGwSWM7SC1oOCWNckaMj1C748/qKEm0r7NV'
url_base = 'https://paper-api.alpaca.markets'

alpaca = tradeapi.REST(api_key_general, api_key_secret, url_base, api_version = 'v2' )
account = alpaca.get_account()

def test():
    print(si.get_live_price("aapl"))

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
    for i in range(len(tickers)):
        tickers[i] = tickers[i].strip()
    return tickers[:185]



def trade():
    api_key_general = 'PKNTALHR7FVNHLKS7S01'
    api_key_secret = 'wnDFd2Ok4CKDRag3VZAgeAxRQGHuq6TWU7IrIqRI'
    url_base = 'https://paper-api.alpaca.markets'
    tickers = save_sp500_tickers()
    alpaca = tradeapi.REST(api_key_general, api_key_secret, url_base, api_version = 'v2' )
    account = alpaca.get_account()
    ticker_list = []
    for tick in tickers:
        ticker_list.append(yf.Ticker(tick))
    indexes = [0, 4, 18, 20, 33, 37, 40, 43, 47, 50, 61, 66, 69, 78, 81, 82, 88, 90, 93, 98, 103, 105, 112, 121, 127, 128, 139, 144, 145, 158, 159, 160, 162, 164, 171, 180, 182]
    for index in sorted(indexes, reverse=True):
        del ticker_list[index]
        del tickers[index]
    length = len(ticker_list)
    data = []
    sell = []
    for i in range(length):
        sell.append(0)
        
    while True:
        if alpaca.get_clock().is_open == True:
            start = time.time()
            for i in range(20):
                stop = time.time()
                print(stop - start,' at iteration: ', i)
                data[i][3] = data[i][2]
                data[i][2] = data[i][1]
                data[i][1] = data[i][0]
                data[i][0] = si.get_live_price(tickers[i])
                if sell[i] == 1:
                    alpaca.submit_order(tickers[i], 10, 'sell', 'market', 'day')
                    sell[i] = 0
                elif data[i][3] > data[i][2]:
                    if data[i][2] > data[i][1]:
                        if data[i][1] <= data[i][0]:
                            alpaca.submit_order(tickers[i], 10, 'buy', 'market', 'day')
                            sell[i] = 1
        else:
            for i in range(length):
                data.append(["","","",""])
            sleep(3600)
            
def quick_trade(ticker):
    data = ["","","",""]
    sell = 0
    while True:
        data[3] = data[2]
        data[2] = data[1]
        data[1] = data[0]
        data[0] = si.get_live_price(ticker)
        if data[3] != "":
            if sell == 1:
                alpaca.submit_order(ticker, 10, 'sell', 'market', 'day')
                data = ["","","",""]
                print('sell')
                sell = 0
            elif data[3] <= data[2]:
                print('Con 1', data[3] , ", ",data[2] , ", ",data[1] , ", ",data[0])
                if data[2] <= data[1]:
                    if data[1] < data[0]:
                        print('buy')
                        alpaca.submit_order(ticker, 10, 'buy', 'market', 'day')
                        sell = 1
        
        

    
        
        