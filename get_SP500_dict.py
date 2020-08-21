#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 21:15:33 2020

@author: coryhunter
"""
import requests
import bs4 as bs

def save_sp500_dict():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    names= []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        names.append(row.findAll('td')[1].text)
    for i in range(len(tickers)):
        tickers[i] = tickers[i].strip()
    dictionary = dict(zip(tickers,names))
    return dictionary
