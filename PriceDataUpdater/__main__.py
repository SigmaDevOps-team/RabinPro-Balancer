# SigmaDevOps
# PriceDataUpdater @ RabinPro Order Balancer
__author__ = ['Saman Mahdanian', 'Mehrafarin Kazemi']

import redis
from binance.client import Client
import parameters as param

redis_client = redis.Redis(**param.redis)

for key in param.binance:
    if (param.binance[key] == 'read_from_redis'):
        param.binance[key] = redis_client.get(param.redis_prefix['binance'] + key.upper())
binance_client = Client(**param.binance)

binance_tickers_json = binance_client.get_all_tickers()
binance_price = {}
for ticker in binance_tickers_json:
    binance_price[ticker['symbol']] = float(ticker['price'])
binance_price['USDTUSDT'] = 1.0

usdt_price = float(redis_client.get(param.redis_prefix['usdt_price']))
keys = str(redis_client.get(param.redis_prefix['pairs']))[2:-1].split(',')
for key in keys:
    asset, base = key.split('/')
    symbol = asset + base
    redis_client.set(
        param.redis_prefix['binance'] + symbol, 
        str(binance_price[symbol] if base != 'IRR' else usdt_price * binance_price[asset + 'USDT'])
    )