#!/usr/bin/python3
from Components import get_args, rasterize

args = get_args()

print("reached here!! args=", args)
exit(0)

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

func_map = {
    'rabin': {
        'push': rabin_push,
        'check': rabin_check,
        'delete': rabin_delete,
    },
    'binance': {
        'push': binance_push,
    }
}

try:
    func_map[args['destination']][args['cmd']](rasterize(args))
except KeyError:
    print('Invalid Command, args=' + str(args))
except Exception as e:
    print(str(e))