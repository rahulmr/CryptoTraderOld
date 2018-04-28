import pandas as pd
import sqlite3
from num2words import num2words
import os

from datetime import date, timedelta
import datetime
import time

import numpy as np

import re

class redditManager():

    def __init__(self, coins = ['BTC', 'DASH', 'DOGE', 'ETH', 'LTC', 'STR', 'XMR', 'XRP']):
        '''
        coins (dictionary): Dictionary containing name of coins
        '''
        self.coinfull = {'BTC': 'bitcoin', 'DASH': 'dashpay', 'DOGE': 'dogecoin', 'ETH': 'ethereum', 'LTC':'litecoin', 'STR': 'stellar', 'XMR': 'monero', 'XRP': 'ripple'}
        self.coins = coins

    def downloader(self):
        pass

    def sql_to_pandas(self):
        pass

    def merge_data(self):
        pass

    