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

from worker import parameters
from worker.components import tll
from worker.components.database import connector

def get_table(database, table):
    database = connector.filter_injection(database)
    table = connector.filter_injection(table)
    tll.debug("write module filter get_table input out of injection", extra=locals())

    cmd = parameters.database_command['get_table'] % table
    tll.debug("read module prepared get_table command", extra = locals())
    return connector.execute(cmd, database)

def get_object_by_parameters(database, table, data):
    database = connector.filter_injection(database)
    table = connector.filter_injection(table)
    data = connector.filter_injection(data)
    assert isinstance(data, dict)
    tll.debug("write module filter get_object_by_parameters input out of injection", extra=locals())

    cmd = parameters.database_command['get_object_by_parameter'] % (
        table,
        ' AND '.join(map(connector.filter_clause, data.keys(), data.values()))
    )
    tll.debug("read module prepared get_object_by_parameters command", extra = locals())
    return connector.execute(cmd, database)

def get_table_columns(database, table):
    database = connector.filter_injection(database)
    table = connector.filter_injection(table)
    tll.debug("write module filter get_table_columns input out of injection", extra=locals())

    cmd = parameters.database_command['get_table_columns'] % (
        table
    )
    tll.debug("read module prepared get_table_columns command", extra = locals())
    result = connector.execute(cmd, database)
    if result['status'] == True:
        result['data'] = [column['Field'] for column in result['data']]
    tll.debug("read module returning the result of get_table_columns", extra=locals())
    return result

# end of file
