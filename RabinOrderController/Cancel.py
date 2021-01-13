# python3 CancelRabinOrder.py <Order_ID>

import json, requests, os
import parameters as param
import redis
from retrying import retry
from time import time
from datetime import datetime


def update_redis(id, filled):
    redis_client = redis.Redis(**param.redis) 
    json_data = json.loads(redis_client.get(param.redis_query['order_data_key']%str(id)))
    json_data['filled'] = filled
    json_data = json.dumps(json_data)

    redis_client.set(param.redis_query['order_data_key']%(str(id)), json_data)
    return

@retry(stop_max_attempt_number = param.max_cancel_retry)
def cancel_order(id):

    url = param.rabin_api['cancel_order']['url']
    payload = {
        'order_id': int(id)
    }

    payload = str(payload)
    payload = payload.replace("'", "\"")

    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IntcInVzZXJfaXBcIjpudWxsLFwidXNlcl9pZFwiOjE0ODIsXCJ1c2VyX3JvbGVcIjoxfSIsImV4cCI6MTYxMDUzODczOCwiaWF0IjoxNjEwNDUyMzM4LCJuYmYiOjE2MTA0NTIzMzh9.7CMo7NxfNh35_SjPjiMAVFVJpKys6mKAv6f-LR7m-2A',
    'Content-Type': 'application/json'
    }
    
    response = requests.request(param.rabin_api['cancel_order']['method'], url, headers=headers, data=payload)
    response = json.loads(response.text)
    assert (response['status'] == 200)

    update_redis(id, response['data']['filled_amount'])
    return 

def do(id):
    cancel_order(id)
    os.system(param.bashcmd['binance']['call_push']%(id))

