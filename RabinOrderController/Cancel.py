# python3 CancelRabinOrder.py <Order_ID>

import tools, parameters, json, requests, os
from database import write
from retrying import retry
from time import time
from datetime import datetime

@retry(stop_max_attempt_number = parameters.max_cancel_retry)
def cancel_order(id):
    pass
    # """
    # payload = {
    #     'order_id': id,
    # }

    # headers = {
    #     'Authorization': 'Bearer ' + parameters.rabinpro_token,
    # }

    # response = requests.request("POST", parameters.cancel_url, headers=headers, data=payload)
    # response = json.loads(response)
    # """
    # response = {
    #     'status' : 200,
    #     'id' : 1,
    #     'filled' : 0.03,
    # }
    # assert (response['status'] == 200)
    # print(write.update(
    #     database = parameters.database,
    #     table    = parameters.database_table_maps['orders'],
    #     data = {
    #         'id': id,
    #     },
    #     upd = {
    #         'status': parameters.canceled_status,
    #         'filled': response['filled'],
    #         'updated_at' : datetime.now(),
    #     },
    # ))

    # return response

def do(id):
    cancel_order(id)
    os.system(bashcmd['binance']['call_push']%(id))

