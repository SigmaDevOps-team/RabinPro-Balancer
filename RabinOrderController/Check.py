# python3 AskRabinOrderFill.py <Order_ID>

import parameters, json, requests, os
from retrying import retry
from time import time


@retry(stop_max_attempt_number = parameters.max_cancel_retry)
def is_finished(id):
    url = parameters.rabin_api['check_order']['url']
    payload = {
        'id': str(id)
    }
    response = requests.request(parameters.rabin_api['check_order']['method'], url, data=payload)
    return response.json()['is_filled'] == '1'


def do(id):
    timer = time()
    while (time() - timer < 2):#parameters.order_age):
        if (is_finished(id)):
            os.system(parameters.bashcmd['binance']['call_push']%(id))
            exit(0)
    os.system(parameters.bashcmd['rabin']['call_cancel']%(str(id)))