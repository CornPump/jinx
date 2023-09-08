import requests
from helpers import smath,files
from enum import Enum


# Enum for Binance's uiklines api list order
class BINANCE_UIKLINES(Enum):
    date,open,high,low,close = range(5)


BINANCE_BASE_ADRESS = 'https://api.binance.com'
KLINE_ADRESS = '/api/v3/uiKlines'
# number of digits Binance API expects for UTC figures
BINANCE_UTC_INT_DIGITS = 13


# returns data for price between two dates, for example 1-1-2022 to 1-10-2022
def get_price_data_by_segment(coin,start_time:int,end_time:int):
    start_time = smath.straighten_digits(start_time,BINANCE_UTC_INT_DIGITS)
    end_time = smath.straighten_digits(end_time, BINANCE_UTC_INT_DIGITS)
    symbol = coin.upper() + 'USDT'
    params = {'symbol': symbol, 'interval': '1d', 'startTime': start_time, 'endTime': end_time}
    url = BINANCE_BASE_ADRESS + KLINE_ADRESS
    r = requests.get(url, params=params).json()
    return r


# returns data for last X days of price
def get_price_data_by_limit(coin,limit):
    symbol = coin.upper() + 'USDT'
    params = {'symbol': symbol, 'interval': '1d', 'limit': limit}
    url = BINANCE_BASE_ADRESS + KLINE_ADRESS
    r = requests.get(url, params=params).json()
    return r

