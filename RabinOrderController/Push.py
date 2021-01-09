# python3 PushRabinOrder.py <Asset> <Base> <Volume> <Fee> <Type>
import tools, parameters, json, requests, time, os
from database import write
from retrying import retry
import time

@retry(stop_max_attempt_number = parameters.max_push_retry)
def push_order(asset, base, volume, fee, type):
    """
    payload = { # bid?
        'asset': asset,
        'amount': volume,
        'bid': fee,
        'type': type,
    }

    headers = {
        'Authorization': 'Bearer ' + parameters.rabinpro_token,
    }
    response = requests.request("POST", parameters.push_url, headers=headers, data=payload)
    response = json.loads(response)
    """
    response = {
        'status' : 200,
        'id' : 1,
    }
    assert (response['status'] == 200)
    print (write.insert(
        database = parameters.database,
        table    = parameters.database_table_maps['orders'],
        data = {
            'id': response['id'],
            'status': parameters.pushed_status,
            'filled' : 0,
        }
    ))

    return response

args = tools.get_args()
response = push_order(**args)
time.sleep(parameters.wait_after_push)
os.system("python3 Cancel.py " + "id=" + str(response['id']))