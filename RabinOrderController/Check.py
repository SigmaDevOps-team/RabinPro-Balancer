# python3 AskRabinOrderFill.py <Order_ID>

import json, requests, os, redis
import parameters as param
from retrying import retry
from time import time


@retry(stop_max_attempt_number = param.max_cancel_retry)
def check_status(id):
    url = param.rabin_api['check_order']['url']
    payload = {
        "order_id" : int(id),
    }

    payload = str(payload)
    payload = payload.replace("'", "\"")

    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IntcInVzZXJfaXBcIjpudWxsLFwidXNlcl9pZFwiOjE0ODIsXCJ1c2VyX3JvbGVcIjoxfSIsImV4cCI6MTYxMDUzODczOCwiaWF0IjoxNjEwNDUyMzM4LCJuYmYiOjE2MTA0NTIzMzh9.7CMo7NxfNh35_SjPjiMAVFVJpKys6mKAv6f-LR7m-2A',
    'Content-Type': 'application/json'
    }

    response = requests.request(param.rabin_api['check_order']['method'], url, headers=headers, data=payload)
    response = json.loads(response.text)

    assert (response['status'] == 200)

    return response['data']['remain'], response['data']['filled']


def update_redis(id, filled):
    redis_client = redis.Redis(**param.redis) 
    
    json_data = json.loads(redis_client.get(param.redis_query['order_data_key']%str(id)))
    json_data['filled'] = filled
    json_data = json.dumps(json_data)

    redis_client.set(param.redis_query['order_data_key']%(str(id)), json_data)

def do(id):
    timer = time()
    while (time() - timer < 2): #param.order_age):
        remain, filled = check_status(id)
        if (remain == 0):
            update_redis(id, filled)
            os.system(param.bashcmd['binance']['call_push']%(id))
            exit(0)
     
    os.system(param.bashcmd['rabin']['call_cancel']%(str(id)))