# python3 PushRabinOrder.py <Asset> <Base> <Volume> <Fee> <Type>
import json, requests, time, os
import parameters as param
from retrying import retry
import redis
import time
from datetime import datetime

@retry(stop_max_attempt_number = param.max_push_retry)
def do(asset, base, volume, fee, type):
    url = param.rabin_api['push_order']['url']
    payload = {
        "currency" : asset,
        "market"   : base,
        "amount"   : volume,
        "bid"      : fee,
        "type"     : type.upper(),
    }

    payload = str(payload)
    payload = payload.replace("'", "\"")

    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IntcInVzZXJfaXBcIjpudWxsLFwidXNlcl9pZFwiOjE0ODIsXCJ1c2VyX3JvbGVcIjoxfSIsImV4cCI6MTYxMDUzODczOCwiaWF0IjoxNjEwNDUyMzM4LCJuYmYiOjE2MTA0NTIzMzh9.7CMo7NxfNh35_SjPjiMAVFVJpKys6mKAv6f-LR7m-2A',
    'Content-Type': 'application/json'
    }
    response = requests.request(param.rabin_api['push_order']['method'], url, headers=headers, data=payload)
    response = json.loads(response.text)
    
    assert (response['status'] == 200)

    # response = {
    #     "data" : {
    #         "order_id" : 10545,
    #     }
    # }

    data = {
        'id'         : response['data']['order_id'],
        # 'status'     : param.order_status['pushed'],
        'filled'     : 0,
        'fee'        : fee,
        # 'created_at' : datetime.now(),
        'asset'      : asset,
        'base'       : base,
        'type'       : type,
    }
    json_data = json.dumps(data)
    # os.system(param.bashcmd['database']['call_push'] % (
    #     param.database, # database
    #     param.database_table_maps['orders'], # table
    #     asset
    # ))

    redis_client = redis.Redis(**param.redis) 
    redis_client.set(param.redis_query['order_data_key']%(str(response['data']['order_id'])), json_data)

    print("push done")
    os.system(param.bashcmd['rabin']['call_check_and_wait']%(str(response['data']['order_id'])))




# data = {'id':1,'status':1,'filled':0.02,'created_at':'kir','asset':'BTC','base':'USDT'}