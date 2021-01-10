#include <string>

using namespace std;

struct parameters {
    const string REDIS_ADDRESS               = "tcp://127.0.0.1:6379";
    const string MODULE_REDIS_PREFIX         = "RPB:";

    const string BINANCE_PRICE_REDIS_PREFIX  = "BINANCE:";
    const string BINANCE_PRICE_REDIS_QUERY_PREFIX =
        MODULE_REDIS_PREFIX + BINANCE_PRICE_REDIS_PREFIX;

    const string PAIR_LIST_REDIS_ENDPOINT    = "PAIRS";
    const string PAIR_LIST_REDIS_QUERY       =
        MODULE_REDIS_PREFIX + PAIR_LIST_REDIS_ENDPOINT;

    const string PATTERNS_LOCATION           = "./patterns";
    const string PATTERN_NAME_REDIS_ENDPOINT = "PATTERN_NAME";
    const string PATTERN_NAME_REDIS_QUERY =
        MODULE_REDIS_PREFIX + PATTERN_NAME_REDIS_ENDPOINT;

    const string BUDGET_REDIS_PREFIX         = "BUDGET:";
    const string BUDGET_REDIS_BASE_SUFFIX    = ":BASE";
    const string BUDGET_REDIS_ASSET_SUFFIX   = ":ASSET";

    const int PUSH_ORDER_NUMBERIC_INPUT_LEN  = 12;
    const string PUSH_ORDER_SYSTEM_PREFIX    = "../OrderController.py rabin push";
    const string PUSH_ORDER_VOLUME_PREFIX    = " volume=";
    const string PUSH_ORDER_ASSET_PREFIX     = " asset=";
    const string PUSH_ORDER_BASE_PREFIX      = " base=";
    const string PUSH_ORDER_RATE_PREFIX      = " fee=";
    const string PUSH_ORDER_TYPE_PREFIX      = " type=";
    const string RUN_IN_BACKGROUND           = " &";
};