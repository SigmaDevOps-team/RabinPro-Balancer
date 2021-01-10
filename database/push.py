
from database import write
import json

def do(args):
    database = args['db']
    table = args['table']
    data = json.loads(args['data'])
    
    write.insert(database, table, data)

