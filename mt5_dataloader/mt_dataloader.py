"""
This module contains methods to extract historical price data from the MetaTrader5 Terminal using the Python 
MetaTrader5 API. 
"""
import os 
import datetime
from typing import Optional, List, Union, Any, Tuple

import pandas as pd
import MetaTrader5 as mt5
from tenacity import retry, stop_after_attempt, retry_if_exception_type

from .mt_pricedata import PriceData
from .mt_utils import MTRequests, MTResolutions, SymbolCategories
from constants import constants as c


class MTDataLoader: 

    valid_requests = [request.value for request in MTRequests.__members__.values()]
    valid_resolutions = [resolution.value for resolution in MTResolutions.__members__.values()]

    def __init__(
            self, 
            path: str = None,
            envpath_key: str = 'MT5_PATH'):
        """ 
        Initialize instance variables 

        Parameters
        ----------
            path:str = None 
                Path to MT5 executable. Paths are stored in `mt_paths.py`

                If no path is specified (None), default path will be taken from environment variable specified by the
                key: `MT5_PATH`

            envpath_key:str = MT5_PATH
                Default key for environment variable if no path is specified for MT5 executable. 
        """

        self.path = self.get_path(envpath_key, path)
        self.launch_mt5()
        
        
    @staticmethod
    def get_path(key: str, path: Optional[str]):  
        if path is not None: 
            return path 
        try:
            mt5_path = os.environ[key]
            return mt5_path 
        except Exception as e: 
            print(f"MT5 Path not found. Add MT5 path to environment variables. Default Key: MT5_PATH. Exception: {e}")
            return ""

    def launch_mt5(self) -> None: 
        """ 
        Launches the MT5 terminal. This is needed in order to get historical data. 
        """
        if mt5.account_info() is None and self.path is not None: 
            try: 
                launched = mt5.initialize(self.path)
            except Exception as e: 
                raise RuntimeError(f"Failed to launch MetaTrader5. Exception: {e}") 
    
    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(KeyError))
    def get_price_data(
            self,
            symbol: str,
            resolution: Union[str, MTResolutions],
            request_type: Union[str, MTRequests],
            start_date: Optional[Union[datetime.datetime, datetime.date]] = None,
            end_date: Optional[Union[datetime.datetime, datetime.date]] = None,
            start_index: Optional[int] = 0,
            num_bars: Optional[int] = 99000,
            export: Optional[bool] = False) -> Optional[PriceData]:
        # TODO improve docstring
        """
        Fetches price data from MT5 history. 
        

        Parameters
        ----------
            symbol: str
                Symbol to fetch data
            
            resolution: str
                Timeframe/resolution. See MTResolutions 
            
            request_type: str 
                Determines how MT5 will get historical data, either by:
                    1. `pos` - Gets data using the number of candles. Required parameter: `num_bars` 
                    2. `range` - Gets data using a range of dates. Required parameters: `start_date`, `end_date` 
                    3. `date` - Gets data until a specified data. Required parameter: `end_date`

            start_date: datetime
                Start date for historical data. 
                Used when `request_type` is either `date` or `range`
                Ignored when `request_type` is set to `pos`

            end_date: datetime
                End date for historical data. 
                Used when `request_type` is either `date` or `range`  
                Ignored when `request_type` is set to `pos`

            start_index: int 
                First bar to fetch with reference to current open bar. 0 = current bar 
                Used when `request_type` is set to `pos`
            
            num_bars: int 
                Number of bars to fetch. 
                Used when `request_type` is set to `pos`

            export: bool
                Exports data to csv. Not implemented.     
        """

        resolution = self.get_resolution(resolution).value 
        request_type = self.get_request_type(request_type) 
        

        rates = None
        try:
            if request_type == MTRequests.POSITION: 
                # Gets historical data based on position. 
                rates = mt5.copy_rates_from_pos(symbol, resolution, start_index, num_bars)
            
            elif request_type == MTRequests.DATE:
                # Gets historical data based on date 
                if end_date is None:
                    raise ValueError("No end date specified")
                
                end_date = self.__dates_as_datetime(end_date) 
                
                rates = mt5.copy_rates_from(symbol, resolution, end_date, num_bars)
            
            elif request_type == MTRequests.RANGE:
                # Gets historical data based on date range
                if start_date is None or end_date is None:
                    raise ValueError("Incomplete dates. Query requires start date and end date.") 
                
                start_date = self.__dates_as_datetime(start_date) 
                end_date = self.__dates_as_datetime(end_date) 

                if end_date < start_date:
                    raise ValueError(f"Invalid Dates. Start Date: {start_date} cannot be greater than End Date: \
                        {end_date}.")
                
                
                rates = mt5.copy_rates_range(symbol, resolution, start_date, end_date)

            else:
                # This is unlikely to happen since if request is invalid, a KeyError will be thrown
                raise ValueError(f"Something went wrong. Request Type may be invalid")

        except KeyError:
            print(f"No data available for: {symbol} {MTResolutions.timeframe(resolution=resolution)}") 

            return None

        if rates is None: 
            print(f"No data available for: {symbol} {MTResolutions.timeframe(resolution=resolution)}") 

            return None 

        df = self.rates_to_frame(rates)
        
        price_data = PriceData(symbol, resolution, df)
        
        return price_data

    @staticmethod 
    def timeframe(resolution: Union[int, MTResolutions]) -> str: 
        if isinstance(resolution, MTResolutions): 
            resolution = resolution.value 

        return MTResolutions.timeframe(resolution=resolution)

    @classmethod 
    def get_resolution(cls, resolution: Union[int, MTResolutions]) -> MTResolutions: 
        if isinstance(resolution, int): 
            if resolution not in cls.valid_resolutions:
                raise ValueError(f"Value not found in valid resolution values. Value: {resolution}")
            resolution = MTResolutions._value2member_map_[resolution]
        elif isinstance(resolution, MTResolutions):
            if resolution not in MTResolutions.__members__.values():
                raise ValueError(f"Value not found in valid resolutions. Value: {resolution}")
        else:
            raise TypeError(f"Invalid type for specified resolution. Only use `int` and `MTResolutions`. Received: {type(resolution)}")
        return resolution  
    
    @classmethod 
    def get_request_type(cls, request_type: Union[str, MTRequests]) -> MTRequests: 
        if isinstance(request_type, str): 
            if request_type not in cls.valid_requests:
                raise ValueError(f"Value not found in valid request values. Value: {request_type}")
            request_type = MTRequests._value2member_map_[request_type]
        elif isinstance(request_type, MTRequests): 
            if request_type not in MTRequests.__members__.values(): 
                raise ValueError(f"Value not found in valid requests. Value: {request_type}")
        else:
            raise TypeError(f"Invalid type for specified request. Only use `str` and `MTRequests`")
        return request_type
    
    @staticmethod
    def __dates_as_datetime(target: Union[datetime.datetime, datetime.date]) -> datetime.datetime: 
        if isinstance(target, datetime.datetime):
            return target 
        try:
            return datetime.datetime(year=target.year, month=target.month, day=target.day) 
        except AttributeError: 
            raise TypeError(f"Invalid datetime type for: {target}. Value must be: `datetime.datetime` or `datetime.date`")

    @staticmethod 
    def rates_to_frame(rates: Any) -> pd.DataFrame:
        """ 
        Converts raw rates into dataframe with OHLC columns.
        """
        data = pd.DataFrame(data=rates)
        data['time'] = pd.to_datetime(data['time'], unit='s')
        data = data.loc[:, ['time', 'open', 'high', 'low', 'close', 'spread']]
        data = data.set_index('time', drop=True)
        data.index.name = 'date'

        return data 

    @staticmethod 
    def get_symbols(category: str) -> List[str]:
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
    def categories() -> List[str]:
        """ 
        Gets list of categories derived from symbols path
        """
        symbols = mt5.symbols_get()
        cats = list()
        for sym in symbols:
            sym_dict = sym._asdict()
            cat = '\\'.join(sym_dict['path'].split('\\')[:-1])
            
            cats.append(cat)
        
        return list(set(cats)) 
    

    @classmethod 
    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(KeyError))
    def get_symbol_properties(cls, symbol: str) -> Tuple[float, float]: 

        symbol_info = mt5.symbol_info(symbol)._asdict()
        tick_value = symbol_info[c.TICK_VALUE]
        trade_points = symbol_info[c.POINT]
        return tick_value, trade_points
    
