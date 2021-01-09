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

from randstr import randstr

import parameters
from database import connector, read

def insert(database, table, data):
    database = connector.filter_injection(database)
    table    = connector.filter_injection(table)
    data     = connector.filter_injection(data)
    assert isinstance(data, dict)
    data['insert_hash'] = randstr(
        parameters.database_config['insert_hash_length']
    )
    cmd = parameters.database_command['insert'] % (
        table,
        ', '.join(map(connector.filter_key_clause, data.keys())),
        ', '.join(map(connector.filter_value_clause, data.values()))
    )
    result = connector.execute(cmd, database)
    result['object'] = read.get_object_by_parameters(database, table, data)
    if result['object']['success'] == 'failure':
        result['success'] = 'failure'

    return result


def delete(database, table, data):
    database = connector.filter_injection(database)
    table    = connector.filter_injection(table)
    data     = connector.filter_injection(data)
    assert isinstance(data, dict)
    
    cmd = parameters.database_command['delete'] % (
        table,
        '  AND  '.join(map(connector.filter_clause, data.keys(), data.values()))
    )
    return connector.execute(cmd, database)


def update(database, table, data, upd):
    database = connector.filter_injection(database)
    table    = connector.filter_injection(table)
    data     = connector.filter_injection(data)
    upd      = connector.filter_injection(upd)
    assert isinstance(data, dict)
    assert isinstance(upd, dict)

    cmd = parameters.database_command['update'] % (
        table,
        ', '.join(map(connector.filter_clause, upd.keys(), upd.values())),
        '  AND  '.join(map(connector.filter_clause, data.keys(), data.values()))
    )
    return connector.execute(cmd, database)

# end of file
