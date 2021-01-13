#include <cmath>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <sw/redis++/redis++.h>
#include <iostream>

#include "Constants.h"
#include "OrderData.h"

using namespace sw::redis;
parameters od_param;

int remaining_floating_point(long double x) {
    int len = log10(x);
    return max(0, od_param.PUSH_ORDER_NUMBERIC_INPUT_LEN - len);
}

bool OrderTemplate::is_sell() {
    return type == 0;
}

bool OrderTemplate::is_buy() {
    return !is_sell();
}

string OrderTemplate::get_type() {
    return is_sell()? "sell":"buy";
}

void OrderTemplate::push(long double base_budget, long double rate, string asset, string base){
    stringstream query;
    cout << "forking query" << endl;
    query << od_param.PUSH_ORDER_SYSTEM_PREFIX;
    query << od_param.PUSH_ORDER_ASSET_PREFIX << asset;
    query << od_param.PUSH_ORDER_BASE_PREFIX  << base;
    query << od_param.PUSH_ORDER_TYPE_PREFIX  << get_type();

    long double volume = (base_budget / rate) * VolumeFraction;
    rate *= 1 + PriceMargin;

    query << fixed << setprecision(remaining_floating_point(rate));
    query << od_param.PUSH_ORDER_RATE_PREFIX  << rate;
    query << fixed << setprecision(remaining_floating_point(volume));
    query << od_param.PUSH_ORDER_VOLUME_PREFIX << volume;
    
    query << od_param.RUN_IN_BACKGROUND << endl;
    system(query.str().c_str());
}

void OrderPattern::read_from_file(ifstream &pattern_defenition) {
    double vf, pm;
    string type, header, devnull;
    while (pattern_defenition >> header)
        if (header[0] == '>') {
            pattern_defenition >> vf >> devnull >> type >> devnull >> pm >> devnull;
            orders.push_back(OrderTemplate(type, vf, pm / 100.0));
        } else
            getline(pattern_defenition, type);
    make_standard();
}

void OrderPattern::apply(string asset, string base) {
    AppliedBase = base;
    AppliedAsset = asset;
}

void OrderPattern::read_budget() {
    Redis redis(od_param.REDIS_ADDRESS);
    cout << od_param.MODULE_REDIS_PREFIX + od_param.BUDGET_REDIS_PREFIX + AppliedAsset + AppliedBase + od_param.BUDGET_REDIS_BASE_SUFFIX << endl;
    BaseBudget  = stod(*redis.get(od_param.MODULE_REDIS_PREFIX
                                + od_param.BUDGET_REDIS_PREFIX 
                                + AppliedAsset + AppliedBase 
                                + od_param.BUDGET_REDIS_BASE_SUFFIX
                                )
                    );
    AssetBudget = stod(*redis.get(od_param.MODULE_REDIS_PREFIX
                                + od_param.BUDGET_REDIS_PREFIX 
                                + AppliedAsset + AppliedBase
                                + od_param.BUDGET_REDIS_ASSET_SUFFIX
                                )
                    );
    cout << BaseBudget << ' ' << AssetBudget << endl;
}

void OrderPattern::push_orders(PriceDataset &pd) {
    cout << "$$" << AppliedAsset + AppliedBase << endl;
    long double rate = pd.getPrice(AppliedAsset + AppliedBase);
    cout << "~ " << rate << endl;
    for (OrderTemplate &o: orders) {
        o.push(
            o.is_buy()? BaseBudget : (AssetBudget * rate),
            rate,
            AppliedAsset,
            AppliedBase
        );
    }
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