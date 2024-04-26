# MT5 Dataloader: A module for fetching historical market data from the MetaTrader5 Platform 

Integrates with MetaTrader 5 to fetch symbol or historical data. 

## Usage 

Prices can be retrieved through the following: 
1. Position - Candle offsets from latest candle
2. Date - Gets data until the specified `end_date` with the number of bars specified by `num_bars`
3. Range - Gets data within the specified date range with `start_date` and `end_date` 

### **Fetching data by position**
```python
# Instantiate the class  
mt = MTDataLoader()

# Data to request 
symbol = "GBPUSD" # Requested symbol
resolution = mt.resolutions.RESOLUTION_H1 # H1 Timeframe
request_type = mt.request.position # Request by position
num_bars = 100 # Number of bars to return 

# Returns a PriceData object 
price = mt.get_price_data(symbol, resolution, request_type,num_bars=num_bars) 

# Displays first 5 rows of requested data
price.data.head()
```

### **Fetching data by date** 
```python
#Instantiate the class 
mt = MTDataLoader()

# Data to request
symbol = "GBPUSD" # Requested symbol
resolution = mt.resolutions.RESOLUTION_M5 # M5 Timeframe
request_type=mt.request.date # Request by date
num_bars=100 # Number of bars to return 

# Returns a PriceData object 
price=mt.get_price_data(symbol, resolution, request_type, end_date=dt(2024,1,1), num_bars=num_bars)

# Displays first 5 rows of requested data 
price.data.head()
```

### **Price By Range**
```python
#Instantiate the class
mt = MTDataLoader()

# Data to request 
symbol = "GBPUSD" # Requested symbol
resolution = mt.resolutions.RESOLUTION_M30 # M30 Timeframe
request_type = mt.request.range # Request by range
start_date = dt(2024,1,1) # Start Date
end_date = dt(2024,4,1) # End Date

# Returns a PriceData object
price = mt.get_price_data(symbol, resolution, request_type, start_date=start_date, end_date=end_date)

# Displays the first 5 rows of requested data
price.data.head()
```

## **Other Functions**
### **Fetching symbol names by category**
```python

# Select a category from SymbolCategories class 
category = SymbolCategories().fxmajors

# Returns a list of symbols with the specified category
print(mt.get_symbols(category))

# Symbols under the fxmajors category 
['EURUSD', 'GBPUSD', 'USDCHF', 'USDJPY', 'USDCAD', 'AUDUSD']
```


## **PriceData** 

### **Data Info** 
```python 
# Request Price Data
price = mt.get_price_data(symbol, resolution, request_type, start_date=start_date, end_date=end_date)

# Prints Price Info
price.info() 

Symbol: GBPUSD
Resolution: h1
Length: 1536
```

### **Price Plot** 
```python
# Request Price Data
price = mt.get_price_data(symbol, resolution, request_type, start_date=start_date, end_date=end_date)

# Plots the close price of requested data
price.show_plot(kind='line', src='close')
```