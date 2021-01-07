#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <dirent.h>
#include <sw/redis++/redis++.h>

#include "Constants.h"
#include "Components.h"
#include "PriceControllers.h"

using namespace sw::redis;
using namespace std;
parameters param;


struct OrderTemplate {
    int type; // 0 for sell, 1 for buy
    double VolumeFraction, PriceMargin;

    OrderTemplate (string _t, double _vf, double _pm) {
        type = (_t == "Sell" or _t == "sell")? 0:1;
        PriceMargin = _pm; VolumeFraction = _vf;
    }

    bool is_sell();
    bool is_buy();
    string get_type();
};

bool OrderTemplate::is_sell() {
    return type == 0;
}

bool OrderTemplate::is_buy() {
    return !is_buy();
}

string OrderTemplate::get_type() {
    return is_sell()? "Sell":"Buy";
}

struct OrderPattern {
    vector <OrderTemplate> orders;

    void read_from_file(ifstream&);
    void generate_from_file(); // TODO
    void make_standard();
};

void OrderPattern::read_from_file(ifstream &pattern_defenition) {
    double vf, pm;
    string type, header, devnull;
    while (pattern_defenition >> header)
        if (header[0] == '>') {
            pattern_defenition >> vf >> devnull >> type >> devnull >> pm >> devnull;
            orders.push_back(OrderTemplate(type, vf, pm));
        } else
            getline(pattern_defenition, type);
    make_standard();
}

void OrderPattern::make_standard() {
    double sigma[2] = {0.0, 0.0};
    for (auto &x: orders)
        sigma[x.type] += x.VolumeFraction;
    
    double gain[2] = {0.0, 0.0};
    for (int i: {0, 1})
        gain[i] = 1.0 / sigma[i];
    for (auto &x: orders)
        x.VolumeFraction *= gain[x.type];
}


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
