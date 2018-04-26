import pandas as pd

from CryptoScraper import cryptoDownloader

class TestcryptoDownloader:
    
    def test_download(self):
        '''
        Tests all functionality as a whole
        '''
        try:
            cd = cryptoDownloader('LTC')
            cd.download()          
        except:
            print('Poloniex might be blocking your requests');
            
            
        #read file. Asssert size  
        btc = pd.read_csv('CryptoScraper/cache/BTC.csv');
        ltc = pd.read_csv('CryptoScraper/cache/LTC.csv');
        
        diff = btc['Date'] - btc.shift(1)['Date'].fillna(method ='bfill').astype(int)       
        assert(sum(diff != 3600.0) == 1)
        
        diff2 = ltc['Date'] - ltc.shift(1)['Date'].fillna(method ='bfill').astype(int)       
        assert(sum(diff2 != 3600.0) == 1)