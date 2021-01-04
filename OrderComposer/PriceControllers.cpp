#include "Constants.h"
#include "Components.h"
#include "PriceControllers.h"
#include <sw/redis++/redis++.h>

using namespace sw::redis;
parameters pc_param;

double Price::get_value()
{
    if (cache_usage < 10) // check if cache is overaged and expired
        return value;
    cache_usage = 0;

    Redis redis(pc_param.REDIS_ADDRESS);
    string query = pc_param.BINANCE_PRICE_REDIS_QUERY_PREFIX + symbol();

    auto val = redis.get(query);
    if (!val)
    {
        found_exception("Unable to Fetch Price from Redis: " + symbol());
    }
    value = stod(*val);
    return stod(*val);
}

string Price::symbol()
{
    return name + base;
}

double PriceDataset::getPrice(int id)
{
    return dataset[id]->get_value();
}

double PriceDataset::getPrice(string name)
{
    int id = indices[name];
    return getPrice(id);
}

double PriceDataset::operator[](int id)
{
    return getPrice(id);
}

double PriceDataset::operator[](string name)
{
    return getPrice(name);
}

int PriceDataset::add(string name, string base)
{
    int new_id = dataset.size();
    Price *data = new Price(new_id, name, base);
    dataset.push_back(data);
    indices[name + base] = new_id;
    return new_id;
}

int PriceDataset::add(pair<string, string> trade_pair)
{
    return add(trade_pair.first, trade_pair.second);
}