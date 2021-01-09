import sys

def get_args():
    args = sys.argv[1:]
    response = {}
    for query in args:
        if '=' in query:
            a = query.split('=')
            response[a[0]] = a[1]
        else:
            if 'destination' in response:
                response['cmd'] = query
            else:
                response['destination'] = query
    return response

def rasterize(response):
    del response['cmd']
    del response['destination']
    return response

if __name__ == '__main__':
    print(get_args())