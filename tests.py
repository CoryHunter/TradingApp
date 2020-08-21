#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:09:45 2020

@author: coryhunter
"""

import alpaca_trade_api as alpaca
import pandas as pd
from datetime import time

API_Key = 'PKBTN53IP2NBCGQD2UIX'
Secret_Key = 'HKLteZpkwLbQHQYbkCJa7Zwx3vM9VFXhTSANYoFV'

api = alpaca.REST(API_Key, Secret_Key, base_url = 'https://paper-api.alpaca.markets')
DF = api.get_portfolio_history(timeframe="1D",period ="1W").df.equity.iloc[-2]
print(DF)   


