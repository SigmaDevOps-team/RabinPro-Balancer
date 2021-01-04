#include <string>
#include <vector>
#include <iostream>
#include <sw/redis++/redis++.h>

#include "Constants.h"
#include "Components.h"
#include "PriceControllers.h"

using namespace sw::redis;
using namespace std;
parameters param;

void GetPrices(PriceDataset&);
void ComposeAndPushOrders(PriceDataset);
vector<pair<string, string>>* GetPairs();

int main() {
    PriceDataset pd;
    GetPrices(pd);
}

void GetPrices(PriceDataset &pd) {
    auto pairs = GetPairs();
    for (auto trade_pair: *pairs) {
        int id = pd.add(trade_pair);
        cout << pd[id] << endl;
    }
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

