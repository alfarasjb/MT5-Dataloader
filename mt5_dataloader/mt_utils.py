import MetaTrader5 as mt5
from enum import Enum


class MTRequests(Enum):
    POSITION = "pos"
    DATE = "date"
    RANGE = "range"
    
    
class MTResolutions(Enum): 
    RESOLUTION_M1 = mt5.TIMEFRAME_M1
    RESOLUTION_M5 = mt5.TIMEFRAME_M5
    RESOLUTION_M15 = mt5.TIMEFRAME_M15
    RESOLUTION_M30 = mt5.TIMEFRAME_M30
    RESOLUTION_H1 = mt5.TIMEFRAME_H1
    RESOLUTION_H4 = mt5.TIMEFRAME_H4
    RESOLUTION_D1 = mt5.TIMEFRAME_D1
    RESOLUTION_W1 = mt5.TIMEFRAME_W1
    RESOLUTION_MN1 = mt5.TIMEFRAME_MN1
    
    @staticmethod
    def timeframe(resolution): 
        tf_converter = {
            mt5.TIMEFRAME_M1: "m1",
            mt5.TIMEFRAME_M5: "m5",
            mt5.TIMEFRAME_M15: "m15",
            mt5.TIMEFRAME_M30: "m30",
            mt5.TIMEFRAME_H1: "h1",
            mt5.TIMEFRAME_H4: "h4",
            mt5.TIMEFRAME_D1: "d1",
            mt5.TIMEFRAME_W1: "w1",
            mt5.TIMEFRAME_MN1: "mn1"
        }
        return tf_converter[resolution]


class SymbolCategories(Enum):
    EU_STOCKS = 'EU'
    NYSE = 'NYSE'
    SOFT_COMMODITIES = 'Softs'
    ENERGIES_FUTURES = 'Energies0 Futures'
    CRYPTO = 'Crypto'
    UK_STOCKS = 'UK'
    ENERGIES_SPOT = 'Energies Spot'
    FX_MAJORS = 'FX Majors'
    INDICES_FUTURES = 'Indices Futures'
    BONDS = 'Bonds'
    FX_MINORS = 'FX Minors'
    NASDAQ = 'Nasdaq'
    INDICES_SPOT = 'Indices Spot'
    METALS = 'Metals'
    EXOTICS = 'Exotics'

