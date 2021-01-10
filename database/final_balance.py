from database import read, write
import parameters as param
from randstr import randstr
import os

def do (asset, change):
    try:
        response = read.get_object_by_parameters(
            database=param.database,
            table=param.database_table_maps['final_balances'],
            data= {
                'asset' : asset,
            }
        )
        
        if not response['status']:
            os.system('cat "change_balance %s %s fetch_failed" > ./missed_packets/%s.log'%(
                str(asset),
                str(change),
                str(randstr(25)),
            ))
            return

        response = write.update(
            database=param.database,
            table=param.database_table_maps['final_balances'],
            data = {
                'asset': asset,
            },
            upd = {
                'balance': float(response['data'][0]['balance']) + float(change),
            }
        )

        if not response['status']:
            os.system('cat "change_balance %s %s update_failed" > ./missed_packets/%s.log'%(
                str(asset),
                str(change),
                str(randstr(25)),
            ))
    except Exception as e:
        print(e)

