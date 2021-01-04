#include <string>

using namespace std;

struct parameters {
    const string REDIS_ADDRESS = "tcp://127.0.0.1:6379";
    const string MODULE_REDIS_PREFIX = "RPB:";

    const string BINANCE_PRICE_REDIS_PREFIX = "BINANCE:";
    const string BINANCE_PRICE_REDIS_QUERY_PREFIX =
        MODULE_REDIS_PREFIX + BINANCE_PRICE_REDIS_PREFIX;

    const string PAIR_LIST_REDIS_ENDPOINT = "PAIRS";
    const string PAIR_LIST_REDIS_QUERY =
        MODULE_REDIS_PREFIX + PAIR_LIST_REDIS_ENDPOINT;
};