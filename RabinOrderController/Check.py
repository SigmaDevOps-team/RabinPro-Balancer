# python3 AskRabinOrderFill.py <Order_ID>

import tools, parameters, json, requests, os
from database import write
from retrying import retry
from time import time


@retry(stop_max_attempt_number = parameters.max_cancel_retry)
def push_order(id):
    pass
    # payload = {
    #     'id': id,
    # }

    # headers = {
    #     'Authorization': 'Bearer ' + parameters.rabinpro_token,
    # }

    # response = requests.request("POST", parameters.cancel_url, headers=headers, data=payload)
    # response = json.loads(response)
    # assert (response['status'] == 200)

    # write.update(
    #     database = parameters.database,
    #     table    = parameters.database_table_maps['orders'],
    #     data = {
    #         'id': id,
    #     }
    #     upd = {
    #         'status': parameters.canceled_status
    #     }
    # )

def do(id):
    timer = time
    while (time() - timer < parameters.order_age):
        if (is_finished(id)):
            os.system(parameters.bashcmd['call'])
            exit(0)
    os.system(parameters.bashcmd['rabin']['call_cancel']%(str(id)))