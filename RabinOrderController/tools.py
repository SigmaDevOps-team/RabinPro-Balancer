import sys

 def get_args():
     agrs = sys.agrs
     response = {}
     for query in args:
         a = query.split('=')
         response[a[0]] = a[1]
    return response