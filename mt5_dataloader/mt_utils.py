import MetaTrader5 as mt5
from enum import Enum 

class MTRequests(Enum):
    POSITION="pos"
    DATE="date"
    RANGE="range"
    
    
class MTResolutions(Enum): 
    RESOLUTION_M1=mt5.TIMEFRAME_M1 
    RESOLUTION_M5=mt5.TIMEFRAME_M5 
    RESOLUTION_M15=mt5.TIMEFRAME_M15 
    RESOLUTION_M30=mt5.TIMEFRAME_M30 
    RESOLUTION_H1=mt5.TIMEFRAME_H1 
    RESOLUTION_H4=mt5.TIMEFRAME_H4 
    RESOLUTION_D1=mt5.TIMEFRAME_D1 
    RESOLUTION_W1=mt5.TIMEFRAME_W1 
    RESOLUTION_MN1=mt5.TIMEFRAME_MN1 
    
    @staticmethod
    def timeframe(resolution): 
        tf_converter={
            mt5.TIMEFRAME_M1 : "m1",
            mt5.TIMEFRAME_M5 : "m5",
            mt5.TIMEFRAME_M15 : "m15",
            mt5.TIMEFRAME_M30 : "m30", 
            mt5.TIMEFRAME_H1 : "h1",
            mt5.TIMEFRAME_H4 : "h4",
            mt5.TIMEFRAME_D1 : "d1",
            mt5.TIMEFRAME_W1 : "w1",
            mt5.TIMEFRAME_MN1 : "mn1"
        }
        return tf_converter[resolution]
    
    
class SymbolCategories:
    def __init__(self):
        self.eu_stocks='EU'
        self.nyse='NYSE'
        self.soft_commodities='softs' 
        self.energies_futures='Energies Futures'
        self.crypto = 'Crypto'
        self.uk_stocks='UK'
        self.energies_spot='Energies Spot'
        self.fxmajors="Majors"
        self.indices_futures='Indices Futures'
        self.bonds='Bonds'
        self.fxminors="Minors"
        self.nasdaq='Nasdaq'
        self.indices_spot='Indices Spot'
        self.metals='Metals'
        self.exotics="Exotics"
