# python3 Push.py <Order_ID>
import redis
from binance.client import Client

from database import read
import parameters as param

def do(id):
    order = read.get_object_by_parameters(
        param.database,
        param.database_table_maps['orders'],
        {
            'id': str(id)
        }
    )

    redis_client = redis.Redis(**param.redis)

    for key in param.binance:
        if (param.binance[key] == 'read_from_redis'):
            param.binance[key] = redis_client.get(param.redis_prefix['binance'] + key.upper())
    # binance_client = Client(**param.binance)
    binance_client = Client(
        api_key='wR9FNob7CpHfXFrCOlf6RL47C1tqQfIi6nulFUA60Eu0JyDBPe8SKM27jEuL5HIf',
        api_secret='BvjDUqPosFBhfyJDhocRlXyQ1BOzd8KtZ0bsiIaK0i35Emj9AOaa1XgjQrDfZ39i'
    )

    print(binance_client.order_market(
            symbol = "BTCUSDT",
            side="BUY",
            quantity="1"
        )
    )


