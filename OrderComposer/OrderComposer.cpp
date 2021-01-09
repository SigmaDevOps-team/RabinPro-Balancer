#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <dirent.h>
#include <sw/redis++/redis++.h>

#include "Constants.h"
#include "Components.h"
#include "OrderData.h"

using namespace sw::redis;
using namespace std;
parameters param;

void GetPrices(PriceDataset&);
void ComposeAndPushOrders(PriceDataset);
vector<pair<string, string>>* GetPairs();
void ReadPattern(OrderPattern&);

int main() {
    PriceDataset pd;
    GetPrices(pd);

    OrderPattern op;
    ReadPattern(op);
    cout << op.orders.size() << endl;
    for (OrderTemplate x: op.orders)
        cout << x.is_sell() << ' ' << x.VolumeFraction << endl;
    
    op.apply("BTC", "USDT");
    op.read_budget();
    op.push_orders(pd);    
}

void GetPrices(PriceDataset &pd) {
    auto pairs = GetPairs();
    for (auto trade_pair: *pairs) {
        int id = pd.add(trade_pair);
        cout << pd[id] << endl;
    }
}

void ReadPattern(OrderPattern &p) {
    DIR *pDIR = opendir(param.PATTERNS_LOCATION.c_str());
    Redis redis(param.REDIS_ADDRESS);
    auto pattern_name = redis.get(param.PATTERN_NAME_REDIS_QUERY);
    string dir = param.PATTERNS_LOCATION + "/" + *pattern_name + ".ptrn";
    // TODO: Check if Pattern Defenition File exists -> set default.ptrn

    ifstream pattern_defenition;
    pattern_defenition.open(dir);
    p.read_from_file(pattern_defenition);
    pattern_defenition.close();
}

vector<pair<string, string>>* GetPairs() {
    Redis redis(param.REDIS_ADDRESS);
    auto encoded_pair_list = redis.get(param.PAIR_LIST_REDIS_QUERY);
    if (!encoded_pair_list) {
        found_exception("Unable to Fetch PAIR_LIST");
    }

    char pair_delimiter = ',', base_delimiter = '/';
    auto result = new vector<pair<string, string>>(1);
    string *dest = &result->back().first;

    for (char cursor: *encoded_pair_list)
        if (cursor == base_delimiter) 
            dest = &result->back().second;
        else if (cursor == pair_delimiter) {
            result->push_back(pair<string, string>());
            dest = &result->back().first;
        } else
            *dest += cursor;
    
    return result;
}
