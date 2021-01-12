from database import read
from database import write
import parameters as param
import randstr, os, json

def do(id, data):
    try:
        data = json.loads(data)
        response = read.get_object_by_parameters(
            database = param.database,
            table = param.database_table_maps['orders'],
            data = {
                'id': id,
            }
        )
        
        if not response['status']:
            os.system('cat "update_order %s %s fetch_failed" > ./missed_packets/%s.log'%(
                str(id),
                str(data),
                str(randstr(25)),
            ))
            return

        response = write.update(
            database=param.database,
            table=param.database_table_maps['final_balances'],
            data = {
                'id': id
            },
            upd = data
        )

        if not response['status']:
            os.system('cat "update_order %s %s update_failed" > ./missed_packets/%s.log'%(
                str(id),
                str(data),
                str(randstr(25)),
            ))
    except Exception as e:
        print(e)
        raise e