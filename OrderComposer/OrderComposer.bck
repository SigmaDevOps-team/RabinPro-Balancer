#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <ctime>
#include <chrono>
#include <sw/redis++/redis++.h>



using namespace sw::redis;
using namespace std;


const string REDIS_ADDRESS              = "tcp://127.0.0.1:6379";
const string MODULE_REDIS_PREFIX        = "RPB:";

const string BINANCE_PRICE_REDIS_PREFIX = "BINANCE:";
const string BINANCE_PRICE_REDIS_QUERY_PREFIX = 
    MODULE_REDIS_PREFIX + BINANCE_PRICE_REDIS_PREFIX;

const string PAIR_LIST_REDIS_ENDPOINT   = "PAIRS";
const string PAIR_LIST_REDIS_QUERY      =
    MODULE_REDIS_PREFIX + PAIR_LIST_REDIS_ENDPOINT;



struct Price {
    int id;
    double value;
    int cache_usage;
    string name, base;

    Price(int _id, string _name, string _base) {
        id = _id; name = _name; base = _base;
        cache_usage = 100; value = -1;
    }

    string symbol();
    double get_value();
    void update_symbol(string, string); 
};

struct PriceDataset {
    vector <Price*> dataset;
    map <string, int> indices;

    double getPrice(int);
    double getPrice(string);
    double operator[](int);
    double operator[](string);

    int add(string, string);
    int add(pair<string, string>);
};


void found_exception(string);
void GetPrices(PriceDataset&);
void ComposeAndPushOrders(PriceDataset);
vector<pair<string, string>>* GetPairs();


// DevTools
typedef chrono::steady_clock::time_point _timer;
_timer _snow(){
    return chrono::steady_clock::now();
}
void _coutdiff(_timer s, _timer e = _snow()) {
    cout << "Time difference = ";
    cout << chrono::duration_cast<std::chrono::microseconds>(e - s).count();
    cout << "[µs] = ";
    cout << chrono::duration_cast<std::chrono::nanoseconds>(e - s).count();;
    cout << "[ns]" << endl;
}



int main() {
    Price p(1, "BTC", "USDT");
    cout << p.get_value() << endl;
    
    PriceDataset pd;
    GetPrices(pd);

    // for (auto p: pd.dataset)
    //     cout << p->symbol << ' ' << p->base << ' ' << p->id << ' ' << p->value << endl;

    // ComposeAndPushOrders(pd);
}



void found_exception(string status) {
    cout << status << endl;
    exit(-1);
}

void GetPrices(PriceDataset &pd) {
    auto pairs = GetPairs();
    for (auto trade_pair: *pairs) {
        int id = pd.add(trade_pair);
        cout << pd[id] << endl;
    }
}

vector<pair<string, string>>* GetPairs() {
    Redis redis(REDIS_ADDRESS);
    auto encoded_pair_list = redis.get(PAIR_LIST_REDIS_QUERY);
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



double Price::get_value() {
    if (cache_usage < 10) // check if cache is overaged and expired
        return value;
    cache_usage = 0;
    
    Redis redis(REDIS_ADDRESS);
    string query = BINANCE_PRICE_REDIS_QUERY_PREFIX + symbol();
    
    auto val = redis.get(query);
    if (!val) {
        found_exception("Unable to Fetch Price from Redis: " + symbol());
    }
    value = stod(*val);
    return stod(*val);
}

string Price::symbol() {
    return name + base;
}



double PriceDataset::getPrice(int id) {
    return dataset[id]->get_value();
}

double PriceDataset::getPrice(string name) {
    int id = indices[name];
    return getPrice(id);
}

double PriceDataset::operator[](int id) {
    return getPrice(id);
}

double PriceDataset::operator[](string name) {
    return getPrice(name);
}

int PriceDataset::add(string name, string base) {
    int new_id = dataset.size();
    Price *data = new Price(new_id, name, base);
    dataset.push_back(data);
    indices[name + base] = new_id;
    return new_id;
}

int PriceDataset::add(pair<string, string> trade_pair) {
    return add(trade_pair.first, trade_pair.second);
}