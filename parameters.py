
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

shmaster = 'python3 ../OrderController.py'
bashcmd = {
    'rabin': {
        'call_check_and_wait': shmaster + ' rabin check id=%s &',
        'call_cancel' : shmaster + ' rabin cancel id=%s &',
    },
    'binance': {
        'call_push': shmaster + ' binance push id=%s &',
    },
    'database': {
        'call_push'   : shmaster + ' database push db=%s table=%s data="%s" &',
        'chbalance'   : shmaster + ' database chbalance asset=%s change=%s &',
        'call_update' : shmaster + ' database update id=%s data=%s'
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

rabin_api = {
    'push_order' : {
        'url': 'https://testapi.rabinpro.ir/api/rabinCash/orderAdd',
        'method': 'POST',
    },
    'check_order': {
        'url': 'https://testapi.rabinpro.ir/api/rabinCash/orderStatus',
        'method': 'POST',
    },
    'cancel_order': {
        'url': 'https://testapi.rabinpro.ir/api/rabinCash/cancelOrder',
        'method': 'POST',
    },
}

order_status = {
    'pending'    : 0,
    'pushed'     : 1,
    'picked'     : 2,
    'propagated' : 3,
}

