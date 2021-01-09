# Connector Module
# Database Package
# TroubLenza Project
# SigmaDevOps

__author__ = [
    "Saman Mahdanian",
    "Pedram Sadeghian",
    "Mahdi Hajibeygi"
]
__copy_right__ = "SigmaDevOps"

"""
Notes:
    1. Assertions: [] 
"""

import mysql.connector
from retrying import retry
from datetime import datetime

from worker import parameters
from worker.components import tll

def filter_key_clause(key):
    return '%s'%key

def filter_value_clause(value):
    if value == 'NULL':
        return '%s'%value
    return '"%s"'%value

def filter_clause(key, value):
    if value == 'NULL':
        return '%s is %s'%(key, value)
    return '%s = "%s"'%(key, value)

def filter_injection(data):
    special_cases = {
        'None'  : 'NULL',
        'True'  : '1',
        'False' : '0',
    }
    tll.debug('connector module filter injection', extra=locals())
    
    def filter_str (query_string):
        if type(query_string) == datetime:
            query_string = query_string.strftime('%Y-%m-%d %H:%M:%S')
        
        query_string = str(query_string)

        if query_string in special_cases:
            query_string = special_cases[query_string]

        for char in parameters.special_characters:
            query_string = query_string.replace(char, '_')
        query_string = query_string.replace('\"', '\'')
        return query_string

    if type(data) == dict:
        copy_data = {}
        for key in data:
            copy_data[filter_str(key)] = filter_str(data[key])
        data = dict(copy_data)
    else:
        data = filter_str(data)
    return data

def filter_fetchall(data, description):
    columns = []
    for i in range(len(description)):
        columns.append(description[i][0])
    result = []
    for row in data:
        result.append(dict(zip(columns, row)))
    
    return result

def check(exc):
    tll.warning("connector module faced a problem when connecting to mysql", extra = {'exception' : exc, **locals()})
    return True


@retry(retry_on_exception=check, 
       stop_max_attempt_number=5, wait_fixed=2000)
def _execute(cmd, database):
    tll.debug("connector module trying to connect to mysql")
    connection = mysql.connector.connect(
        **parameters.database_server_config, 
        database=database
    )
    cursor = connection.cursor()
    tll.debug("connector module connected to mysql successfully")
    tll.debug("connector module trying to execute a command", extra=locals())
    cursor.execute(cmd)
    tll.debug("connector module executed command successfully")
    
    try:
        result = {'data': filter_fetchall(cursor.fetchall(), cursor.description)}
        tll.debug("connector module have taken result from mysql and filtered them successfully")
    except mysql.connector.Error as err:
        if str(err) == 'No result set to fetch from.':
            result = {'empty_result' : True}
            tll.debug("connector module result was empty", extra = {'exception' : err})
        else:
            result = {
                'empty_result' : True,
                'success'      : 'failure'    
            }
            tll.error("connector module failed to get result from mysql", extra = {'exception' : err, **locals()})

    connection.commit()
    connection.close()
    tll.debug("connector module connection committed and closed successfully") 
    return result

def execute(cmd, database):
    result = {
        'data'         : None,
        'empty_result' : False,
        'status'       : True,
        'error'        : 'no_error',
        'success'      : 'success'
    }

    try:
        result.update(_execute(cmd, database))
    except Exception as err:
        result.update({
            'status'       : False,
            'error'        : str(err),
            'success'      : 'failure',
            'empty_result' : True
        })
        tll.error("connector module faild to send request to mysql", extra = locals())
    else:
        tll.debug("connector module command execution succeeded", extra = locals())
    finally:
        return result

# end of file
