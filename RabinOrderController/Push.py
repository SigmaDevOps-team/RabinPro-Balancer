# python3 PushRabinOrder.py <Asset> <Base> <Volume> <Fee> <Type>
import json, requests, time, os
import parameters as param
from database import write
from retrying import retry
import redis
import time
from datetime import datetime

@retry(stop_max_attempt_number = param.max_push_retry)
def do(asset, base, volume, fee, type):
    """
    payload = { # bid?
        'asset': asset,
        'amount': volume,
        'bid': fee,
        'type': type,
    }

    headers = {
        'Authorization': 'Bearer ' + param.rabinpro_token,
    }
    response = requests.request("POST", param.push_url, headers=headers, data=payload)
    response = json.loads(response)
    """
    response = {
        'status' : 200,
        'id' : 1,
    }
    assert (response['status'] == 200)

    data = {
        'id'         : response['id'],
        'status'     : param.pushed_status,
        'filled'     : 0,
        'created_at' : datetime.now(),
        'asset'      : asset,
        'base'       : base,
    }
    json_data = json.dumps(data)

    os.system(param.bashcmd['database']['call_push'] % (
        param.database, # database
        param.database_table_maps['orders'], # table
        data #data
    ))

    redis_client = redis.Redis(**param.redis) 
    redis_client.set(param.redis_query['order_data_key']%(str(response['id'])), json_data)

    os.system(param.bashcmd['rabin']['call_check_and_wait'] % (str(response['id'])))




data = {'id':1,'status':1,'filled':0.02,'created_at':'kir','asset':'BTC','base':'USDT'}