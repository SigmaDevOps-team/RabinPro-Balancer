# python3 CancelRabinOrder.py <Order_ID>

import tools, parameters, json, requests, os
from database import write
from retrying import retry
from time import time

@retry(stop_max_attempt_number = parameters.max_cancel_retry)
def cancel_order(id):
    payload = {
        'order_id', id
    }

    headers = {
        'Authorization': 'Bearer ' + parameters.rabinpro_token,
    }

    response = requests.request("POST", parameters.cancel_url, headers=headers, data=payload)
    response = json.loads(response)
    assert (response['status'] == 200)

    write.update(
        database = parameters.database,
        table    = parameters.database_table_maps['orders'],
        data = {
            'id': id,
        }
        upd = {
            'status': parameters.canceled_status
        }
    )

args = tools.get_args()
cancel_order(**args)
os.system("python3 RabinOrderController/Check")