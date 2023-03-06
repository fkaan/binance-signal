import time
import ta
import pandas as pd
from binance.client import Client
from config import key, secret
import requests

#for telegram
token = 'YOUR TELEGRAM TOKEN'
chat_id = 'CHAT ID'

api_key =  key
secret_key = secret
client = Client(api_key, secret_key)


interval = Client.KLINE_INTERVAL_5MINUTE
all_symbols = [symbol['symbol'] for symbol in requests.get("https://api.binance.com/api/v3/exchangeInfo").json()['symbols']]
usdt_symbols = [symbol for symbol in all_symbols if symbol.endswith("USDT") and not (symbol.endswith("BULLUSDT") or symbol.endswith("BEARUSDT") or symbol.endswith("DOWNUSDT") or symbol.endswith("UPUSDT"))]


def get_candlestick_data(symbol, interval):
    
    klines = client.get_historical_klines(symbol, interval, "1 day ago UTC")# getting historical klines
    #convert to dataframe
    df = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms') #convert "Open time" column to datetime
    df.set_index('Open time', inplace=True)# set "Open time" column as index
    df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)# convert other columns to float
    return df

# calculate rsi
def get_rsi(df, window=14):
    df['RSI'] = ta.momentum.RSIIndicator(df["Close"], window).rsi()# talib rsi
    return df

# main loop
while True:
    for symbol in usdt_symbols:
        # candlestick data
        df = get_candlestick_data(symbol, interval)
        # calculate RSI
        df = get_rsi(df)
        # Get the latest RSI value
        try:
            latest_rsi = df['RSI'].iloc[-1]
        except IndexError:
            print(symbol)
            continue

        # give a signal on telegram for possible rsi divergences to check it 
        if latest_rsi > 75 :
               
                message = f"{symbol} RSI değeri : {latest_rsi:.2f} - \nPotansiyel Negatif Uyumsuzluk. 🔴"
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
                print(requests.get(url).json())  
        elif latest_rsi < 30 :
                message = f"{symbol} RSI değeri : {latest_rsi:.2f} - \nPotansiyel Pozitif Uyumsuzluk. 🟢"
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
                print(requests.get(url).json())  

    time.sleep(150)
