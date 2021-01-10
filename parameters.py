# URLs
url = 'https://testapi.rabinpro.ir'
push_url = url+'/api/rabinCash/buy/add'

# token
rabinpro_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IntcInVzZXJfaXBcIjpudWxsLFwidXNlcl9pZFwiOjE0NDEsXCJ1c2VyX3JvbGVcIjpudWxsfSIsImV4cCI6MTYxMDI4NTgxMiwiaWF0IjoxNjEwMTk5NDEyLCJuYmYiOjE2MTAxOTk0MTJ9.RszBv3p6_6eg7AXh1p-gl4Oqn2ZPRv0PJZQ66pB0G9U'

# database
database = 'rabinpro_balancer'
database_table_maps = {
    'orders': 'orders',
    'final_balances': 'final_balances',
}
special_characters = ';!@#$%^&*<>|\\/'
database_server_config = {
    'user'               : 'root',
    'password'           : '',
    'host'               : 'localhost',
    'connect_timeout'    : 15,
}
database_command = {
    'get_table'               : 'SELECT * FROM %s',
    'get_object_by_parameter' : 'SELECT * FROM %s WHERE %s',
    'get_table_columns'       : 'SHOW COLUMNS FROM %s',
    'insert'                  : 'INSERT INTO %s (%s) VALUES (%s)',
    'delete'                  : 'DELETE FROM %s WHERE %s',
    'update'                  : 'UPDATE %s SET %s WHERE %s',
}
database_config = {
    'insert_hash_length' : 10,
}

#
max_push_retry = 3
max_cancel_retry = 5
wait_after_push = 3

#
pushed_status = 1
canceled_status = 2

shmaster = './OrderController.py'
bashcmd = {
    'rabin': {
        'call_check_and_wait': shmaster + ' rabin check id=%s &',
        'call_cancel' : shmaster + ' rabin cancel id=%s &',
    },
    'binance': {
        'call_push': shmaster + ' binance push id=%s &',
    },
    'database': {
        'call_push': shmaster + ' database push db=%s table=%s data="%s" &',
        'chbalance': shmaster + ' database chbalance asset=%s change=%s &',
    }
}

order_age = 60 # age in seconds

redis_query = {
    'order_data_key': 'RPB:ORDERS:%s',
}

redis = {
    'host' : 'localhost',
    'port' : 6379,
    'db'   : 0,
}