# python3 Push.py <Order_ID>
import redis
from binance.client import Client
import json, os
import randstr

# from database import read
import parameters as param

def change(asset, change):
    # os.system(param.bashcmd['database']['chbalance'] % (asset, str(change)))
    print (asset, change)

def do(id):
    id = str(id)

    # redis_client = redis.Redis(**param.redis)

    # for key in param.binance:
    #     if (param.binance[key] == 'read_from_redis'):
    #         param.binance[key] = redis_client.get(param.redis_prefix['binance'] + key.upper())
    # binance_client = Client(**param.binance)
    binance_client = Client(
        api_key='wR9FNob7CpHfXFrCOlf6RL47C1tqQfIi6nulFUA60Eu0JyDBPe8SKM27jEuL5HIf',
        api_secret='BvjDUqPosFBhfyJDhocRlXyQ1BOzd8KtZ0bsiIaK0i35Emj9AOaa1XgjQrDfZ39i'
    )

    redis_client = redis.Redis(**param.redis) 
    redis_data = redis_client.get(param.redis_query['order_data_key']%(id))
    data = json.loads(redis_data)

    symbol = data['asset'] + data['base']
    side = data['type'].upper()
    quantity = float(data['filled'])

    response = binance_client.order_market(
        symbol = symbol,
        side = side,
        quantity = quantity
    )

    if 'fills' not in response:
        os.system('cat "binance_order %s %s %s call_failed" > ./missed_packets/%s.log'%(
            symbol, side, quantity,
            str(randstr(25)),
        ))
    
    for fill in response['fills']:
        change(
            data['asset'], 
            float(fill['qty']) * (1 if data['type'].lower() == 'buy' else -1)
        )
        change(
            data['base'],
            float(fill['qty']) * float(fill['price']) *
                (-1 if data['type'].lower() == 'buy' else 1)
        )
        change(
            fill['commissionAsset'],
            -float(fill['commission'])
        )

    print(response)
    







