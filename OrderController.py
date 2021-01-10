#!/usr/bin/python3
from Components import get_args, rasterize

args = get_args()

print("reached here!! args=", args)

def rabin_push(args):
    from RabinOrderController import Push
    Push.do(**args)

def rabin_check(args):
    from RabinOrderController import Check
    Check.do(**args)

def rabin_delete(args):
    from RabinOrderController import Delete
    Delete.do(**args)

def binance_push(args):
    from BinanceOrderController import Push
    Push.do(**args)

def database_push(args):
    from database import push
    push.do(**args)

def database_change_final_balance(args):
    from database import final_balance
    final_balance.do(**args)

func_map = {
    'rabin': {
        'push': rabin_push,
        'check': rabin_check,
        'delete': rabin_delete,
    },
    'binance': {
        'push': binance_push,
    },
    'database': {
        'push': database_push,
        'chbalance' : database_change_final_balance,
    }
}

try:
    func_map[args['destination']][args['cmd']](rasterize(args))
except KeyError:
    print('Invalid Command, args=' + str(args))
except Exception as e:
    print(str(e))