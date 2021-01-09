# python3 PushRabinOrder.py <Asset> <Base> <Volume> <Fee> <Type>
import tools, parameters, json, requests, time, os
from database import write
from retrying import retry
from time import time

@retry(stop_max_attempt_number = parameters.max_push_retry)
def push_order(asset, base, volume, fee, type):
    payload = { # bid?
        'asset': asset,
        'amount': volume
        'bid': fee,
        'type': type,
    }

    headers = {
        'Authorization': 'Bearer ' + parameters.rabinpro_token,
    }

    response = requests.request("POST", parameters.push_url, headers=headers, data=payload)
    response = json.loads(response)
    assert (response['status'] == 200)

    write.insert(
        database = parameters.database,
        table    = parameters.database_table_maps['orders'],
        data = {
            'id': response['id'],
            'status': parameters.pushed_status
        }
    )

    return response

args = tools.get_args()
response = push_order(**args)
time.sleep(parameters.wait_after_push)
os.system("python3 RabinOrderController/Cancel " + str(response['id']))