import pandas as pd
import numpy as np

import time
import datetime

import os

from TechnicalAnalysis import TechnicalAnalysis 

class addData():
    def __init__(self, dfs):
        self.dfs = dfs
        self.coinfull = {'BTC': 'bitcoin', 'DASH': 'dashpay', 'DOGE': 'dogecoin', 'ETH': 'ethereum', 'LTC':'litecoin', 'STR': 'stellar', 'XMR': 'monero', 'XRP': 'ripple'}


    def data_adder(self, type):
        '''
        type (string):
        google, twitter, reddit, wikipedia
        '''

        #Should not add to 0 columns. fix it. And possibly ffill

        if (type == 'blockchain'):
            print('Adding {} data for {}'.format(type, 'BTC'))
            self.dfs['BTC'] = self.add_blockchain(self.dfs['BTC'])
            
        for key,df in self.dfs.items():
            if (type == 'google'):
                print('Adding {} data for {}'.format(type, key))
                self.dfs[key] = self.add_trends(df, self.coinfull[key])
            elif (type == 'wikipedia'):
                print('Adding {} data for {}'.format(type, key))
                self.dfs[key] = self.add_wikipedia(df, self.coinfull[key])

        #convert to zeros
        for key, df in self.dfs.items():
            df.loc[df['Volume'] <= 0.0001] = 0
            self.dfs[key] = df
            self.dfs[key] = self.dfs[key].fillna(method='ffill')

        return self.dfs

    def add_reddit(self):
        pass
    
    def add_twitter(self):
        pass

    def add_blockchain(self, df):
        '''
        Parameters:
        df (Dataframe):
        Dataframe containing coin price and all
        '''  
        
        files = os.listdir("data_utils\\blockchain_data\\bitcoin")

        dfBlock = pd.read_csv('data_utils\\blockchain_data\\bitcoin\\difficulty.csv', header=None)

        dfBlock.columns = ['Date', 'difficulty']
        
        for file in files:
            if file != 'difficulty.csv':
                tDf = pd.read_csv('data_utils\\blockchain_data\\bitcoin\\{}'.format(file), header=None)

                dfBlock[file[:-4]] = tDf[1]
                
        dfBlock['Date'] = dfBlock['Date'].apply(lambda x: int(time.mktime(datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").timetuple())))
        
        
        dfBlock = dfBlock.ffill()
        
        regFeatures = self.addIrregularFeatures(df, dfBlock)
        
        df = df.join(regFeatures)
        
        return df

    def add_wikipedia(self, df, coinfull):
        '''
        Parameters:
        df (Dataframe):
        Dataframe containing coin price and all

        coinfull (string):
        Full name in small like bitcoin
        '''  
        
        wikiDf = pd.read_csv('data_utils\\wikipedia_data\\pageviews.csv')[['Date', coinfull]]
        wikiDf['Date'] = wikiDf['Date'].apply(lambda x: int(time.mktime(datetime.datetime.strptime(x, "%Y-%M-%d").timetuple())))
        wikiDf = wikiDf.rename(columns={coinfull: 'Wikipedia View'})
        
        regFeatures = self.addIrregularFeatures(df, wikiDf)
        
        df = df.join(regFeatures)
        
        return df

    def add_trends(self, df, coinfull):
        '''
        Parameters:
        df (Dataframe):
        Dataframe containing coin price and all

        coinfull (string):
        Full name in small like bitcoin
        '''
        trend = pd.read_csv('data_utils\\trends_data\\{}.csv'.format(coinfull))
        trend = trend[::-1] #reverse
        trend = trend.reset_index(drop=True)
        
        trend['Date'] = trend['date'].apply(lambda x: int(time.mktime(datetime.datetime.strptime(x, "%Y-%M-%d").timetuple())))
        trend = trend.drop('date', axis=1)
        
        trend = trend.rename(columns={coinfull: 'Google Trend'})
        
        regFeatures = self.addIrregularFeatures(df, trend.drop('isPartial', axis=1))
        
        df = df.join(regFeatures)
        
        return df


    def addIrregularFeatures(self, df_coin, irregular_data):
        '''
        Parameters:
        ___________
        
        df_coin (DataFrame):
        Dataframe of coin with date as the index.
        
        irregular_data(DataFrame):
        Dataframe with Date as column
        
        Returns:
        Dataframe the same size as df_coin with same date and features from irregular_data at the closest time - forward filled
        '''
        newDf = pd.DataFrame(columns=['Date'])
        newDf['Date'] = df_coin.index
        
        closestDf = pd.DataFrame(columns=['Date'])

        
        #replace with closest date
        for i in range(irregular_data['Date'].shape[0]):
            closestDf = closestDf.append({'Date': newDf.iloc[(newDf['Date'] - irregular_data['Date'].iloc[i]).abs().argsort()[0]]['Date']}, ignore_index=True)
        
        
        newTrends = irregular_data
        newTrends['Date'] = closestDf['Date']

        newTrends = newTrends.set_index('Date')
        newDf = newDf.set_index('Date')
        
        newTrends = newTrends[~newTrends.index.duplicated(keep='last')] #replace duplicates
        test = newDf.join(newTrends).ffill()
        
        return test #can add unit test if time