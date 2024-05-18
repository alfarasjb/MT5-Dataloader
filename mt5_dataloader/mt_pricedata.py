""" 
This module contains a template to building a type of PriceData. Requests to MT5 in getting historical data 
is converted into this object. 
"""

import pandas as pd
import matplotlib.pyplot as plt

from mt_utils import MTResolutions


class PriceData:
    
    def __init__(self, symbol: str, resolution: str, data: pd.DataFrame):
        """ 
        Parameters
        ----------
            symbol: str 
                Symbol of specified data 
            
            resolution: str 
                Resolution of specified data 

            data: pd.DataFrame
                OHLC data 
        """
        self.symbol = symbol
        self.resolution = resolution
        self.timeframe = MTResolutions.timeframe(self.resolution)
        self.data = data

    def info(self) -> None:
        """ 
        Prints data info 
        """
        print(f"Symbol: {self.symbol}")
        print(f"Resolution: {self.timeframe}")
        print(f"Length: {len(self.data)}")

    def show_plot(self, kind: str = 'line', src: str = 'close') -> None:
        """
        if kind == 'line':
            self.data[src].plot(figsize=(12, 6))
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.title(f'{self.symbol} ({src.capitalize()}) - {self.timeframe.upper()}')
        elif kind == 'candle':
            raise NotImplementedError("OHLC plot is not working properly.")
        else: 
            raise ValueError(f"Invalid plot kind.")
        return None 
        for c in self.data.columns:
            if c not in self.cols: 
                raise ValueError(f"{c} not found in columns. Required Columns: {self.cols}")
            
        if len(self.data) > 100:
            print("Showing last 100 rows")
        
        data = self.data.copy().tail(10000)

        fig = go.Figure(data=go.Candlestick(x=data.index, open=data['open'], high=data['high'], low=data['low'], close=data['close']))
        fig.update_layout(width=800, height=500)
        

        fig.show()
        """
        return None


