import requests
import pandas as pd
import ta
from config import key, secret
from binance.client import Client
import time

#for telegram
token = '6092925870:AAF37tv9-LeMo3UPpc3EIvAE6uO2R44uRoo'
chat_id = '-1001709437165'

api_key =  key
secret_key = secret
client = Client(api_key, secret_key)

def find_divergence(symbol):
    #binance api
    url = "https://api.binance.com/api/v3/klines?symbol=" + symbol + "&interval=5m&limit=100"
    response = requests.get(url)
    data = response.json()
    
    #converting df
    df = pd.DataFrame(data, columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
    df[["Open", "High", "Low", "Close"]] = df[["Open", "High", "Low", "Close"]].astype(float)
    
    #calculate rsi with talib
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    
    #divergence calculate 
    bullish_divergence = ((df["Close"].shift(1) < df["Close"]) & (df["RSI"].shift(1) > df["RSI"]) & (df["RSI"] < 30))
    bearish_divergence = ((df["Close"].shift(1) > df["Close"]) & (df["RSI"].shift(1) < df["RSI"]) & (df["RSI"] > 70))
    
    if bullish_divergence.any():
        print(symbol + ": Bullish divergence detected")
        message = f"{symbol} RSI değeri : {df['RSI']}  \nPozitif Uyumsuzluk Sinyali. 🟢"
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        print(requests.get(url).json())  

    elif bearish_divergence.any():
        print(symbol + ": Bearish divergence detected")
        message = f"{symbol} RSI değeri : {df['RSI']} - \nNegatif Uyumsuzluk Sinyali. 🔴"
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        print(requests.get(url).json()) 
    
    else:
        print(symbol + ": No divergence detected" )


url = "https://api.binance.com/api/v3/exchangeInfo"#get a list of all futures market coins from Binance API
response = requests.get(url)
data = response.json()
futures_exchange_info = client.futures_exchange_info()  # request info on all futures symbols
trading_pairs = [info['symbol'] for info in futures_exchange_info['symbols']]

#find divergence
while True :
    for symbol in trading_pairs:
        find_divergence(symbol)
    time.sleep(150)
    
