# Write Module
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
    1. Assertions: [28, 57, 73, 74] 
"""

from randstr import randstr

from worker import parameters
from worker.components import tll
from worker.components.database import connector, read

def insert(database, table, data):
    database = connector.filter_injection(database)
    table    = connector.filter_injection(table)
    data     = connector.filter_injection(data)
    assert isinstance(data, dict)
    data['insert_hash'] = randstr(
        parameters.database_config['insert_hash_length']
    )
    tll.debug("write module filter insert input out of injection", extra=locals())

    cmd = parameters.database_command['insert'] % (
        table,
        ', '.join(map(connector.filter_key_clause, data.keys())),
        ', '.join(map(connector.filter_value_clause, data.values()))
    )
    tll.debug("write module prepared insert command", extra = locals())
    result = connector.execute(cmd, database)
    tll.debug("write module executing insert command and going to read the object")
    result['object'] = read.get_object_by_parameters(database, table, data)
    if result['object']['success'] == 'failure':
        result['success'] = 'failure'

    if result['success'] == 'failure':
        tll.debug("write madule insert command was a failure", extra=locals())
    else:
        tll.debug("write madule insert command was a success", extra=locals())
    return result


def delete(database, table, data):
    database = connector.filter_injection(database)
    table    = connector.filter_injection(table)
    data     = connector.filter_injection(data)
    assert isinstance(data, dict)
    tll.debug("write module filter delete input out of injection", extra=locals())
    
    cmd = parameters.database_command['delete'] % (
        table,
        '  AND  '.join(map(connector.filter_clause, data.keys(), data.values()))
    )
    tll.debug("write module prepared delete command, going to execute...", extra = locals())
    return connector.execute(cmd, database)


def update(database, table, data, upd):
    database = connector.filter_injection(database)
    table    = connector.filter_injection(table)
    data     = connector.filter_injection(data)
    upd      = connector.filter_injection(upd)
    assert isinstance(data, dict)
    assert isinstance(upd, dict)
    tll.debug("write module filter update input out of injection", extra=locals())

    cmd = parameters.database_command['update'] % (
        table,
        ', '.join(map(connector.filter_clause, upd.keys(), upd.values())),
        '  AND  '.join(map(connector.filter_clause, data.keys(), data.values()))
    )
    tll.debug("wtite module prepared update command", extra = locals())
    return connector.execute(cmd, database)

# end of file
