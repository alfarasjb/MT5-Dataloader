import pandas as pd
import MetaTrader5 as mt5
import os 
from .mt_utils import * 
from .mt_pricedata import * 
import datetime


class MTDataLoader: 

    def __init__(self, envpath_key:str = 'MT5_PATH'): 
        try:
            self.path = os.environ[envpath_key]
        except:
            print("MT5 Path not found. Add MT5 path to environment variables. Default Key: MT5_PATH")
            self.path = None 
        if mt5.account_info() is None and self.path is not None: 
            try:
                launched = self.launch_mt5()
            except:
                raise RuntimeError("Failed to launch MetaTrader5")
            
            
        # constants 
        
        self.cols=['date','open','high','low','close','spread']
        
        self.resolutions = MTResolutions()
        self.request = MTRequests()
            
    def launch_mt5(self) -> bool: 
        return mt5.initialize(self.path)
    
        
    def get_price_data(self,
                           symbol:str,
                           resolution:str,
                           request_type:str, 
                           start_date=None,
                           end_date=None, 
                           start_index:int=0,
                           num_bars:int=99000, 
                           export:bool=False) -> pd.DataFrame:

        """
        Fetches price data from MT5 history. 

        Returns a DataFrame 
        """

        rates=None 
        try:
            if request_type == self.request.position: 
                rates = mt5.copy_rates_from_pos(symbol, resolution, start_index, num_bars)
            
            if request_type == self.request.date:
                if end_date is None:
                    raise ValueError("No start date specified")
                
                end_date = self.__dates_as_datetime(end_date) if isinstance(end_date, datetime.date) else end_date
                rates = mt5.copy_rates_from(symbol, resolution, end_date, num_bars)
            
            if request_type == self.request.range:
                if start_date is None or end_date is None:
                    raise ValueError("Incomplete dates. Query requires start date and end date.")
                
                start_date = self.__dates_as_datetime(start_date) if isinstance(start_date, datetime.date) else start_date 
                end_date = self.__dates_as_datetime(end_date) if isinstance(end_date, datetime.date) else end_date
                
                rates = mt5.copy_rates_range(symbol, resolution, start_date, end_date)

            else: 
                if request_type not in self.request.valid_values:
                    raise ValueError(f"Invalid Request Type. Valid Values: {self.request.valid_values}. Input: {request_type}")


        except KeyError:
            print(f"No data available for: {symbol} {MTResolutions().timeframe(resolution=resolution)}") 
        
        if rates is None: 
            print(f"No data available for: {symbol} {MTResolutions().timeframe(resolution=resolution)}") 
            return None 

        df = self.__rates_to_frame(rates) 
        
        price_data = PriceData(symbol, resolution, df)
        
        return price_data
 
    @staticmethod
    def __dates_as_datetime(target:datetime.datetime):
        return datetime.datetime(year=target.year, month=target.month, day=target.day)
    
    @staticmethod 
    def __rates_to_frame(rates) -> pd.DataFrame:
        """ 
        Converts raw rates into dataframe with OHLC columns.
        """
        data = pd.DataFrame(data=rates)
        data['time']=pd.to_datetime(data['time'],unit='s')
        data = data.loc[:,['time','open','high','low','close','spread']]
        data = data.set_index('time', drop=True)
        data.index.name='date'
        return data 
        

    @staticmethod 
    def get_symbols(category:str) -> list:
        """
        Gets list of symbols under a specified category
        """
        symbols = mt5.symbols_get()
        symbols_list = list()
        for sym in symbols: 
            sym_dict = sym._asdict()
            path, name = sym_dict['path'], sym_dict['name']
            if category not in path:
                continue 
            symbols_list.append(name)

        return symbols_list 
    

    
    @staticmethod 
    def categories() -> list:
        """ 
        Gets list of categories derived from symbols path
        """
        symbols=mt5.symbols_get()
        cats=list()
        for sym in symbols:
            sym_dict = sym._asdict()
            cat = '\\'.join(sym_dict['path'].split('\\')[:-1])
            
            cats.append(cat)
        
        return list(set(cats))
