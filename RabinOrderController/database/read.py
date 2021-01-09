# Read Module
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
    1. Assertions: [35] 
"""

import parameters
from database import connector

def get_table(database, table):
    database = connector.filter_injection(database)
    table = connector.filter_injection(table)

    cmd = parameters.database_command['get_table'] % table
    return connector.execute(cmd, database)

def get_object_by_parameters(database, table, data):
    database = connector.filter_injection(database)
    table = connector.filter_injection(table)
    data = connector.filter_injection(data)
    assert isinstance(data, dict)

    cmd = parameters.database_command['get_object_by_parameter'] % (
        table,
        ' AND '.join(map(connector.filter_clause, data.keys(), data.values()))
    )
    return connector.execute(cmd, database)

def get_table_columns(database, table):
    database = connector.filter_injection(database)
    table = connector.filter_injection(table)

    cmd = parameters.database_command['get_table_columns'] % (
        table
    )
    result = connector.execute(cmd, database)
    if result['status'] == True:
        result['data'] = [column['Field'] for column in result['data']]
    return result

# end of file
