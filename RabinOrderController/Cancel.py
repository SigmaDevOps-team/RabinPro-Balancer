# python3 CancelRabinOrder.py <Order_ID>

import parameters, json, requests, os
from retrying import retry
from time import time
from datetime import datetime

@retry(stop_max_attempt_number = parameters.max_cancel_retry)
def cancel_order(id):

    url = parameters.rabin_api['cancel_order']['url']
    payload = {
        'order_id': str(id)
    }
    response = requests.request(parameters.rabin_api['cancel_order']['method'], url, data=payload)
    

    response
    assert (response['status'] == 200)


    

    
    
    

def do(id):
    cancel_order(id)
    os.system(parameters.bashcmd['binance']['call_push']%(id))

