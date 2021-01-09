import sys

def get_args():
    args = sys.argv[1:]
    response = {}
    for query in args:
        a = query.split('=')
        response[a[0]] = a[1]
    return response