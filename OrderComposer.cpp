#include <iostream>
#include <string>
#include <vector>
#include <map>
// #include <sw/redis++/redis++.h>
// using namespace sw::redis;
using namespace std;

struct Price {
    int id;
    double value;
    string symbol, base;

    Price(int _id, string _symbol, string _base,double _value) {
        id = _id; symbol = _symbol; base = _base; value = _value;
    }

    void update_value(double);
    void update_symbol(string); 
};

struct PriceDataset {
    vector <Price*> dataset;
    map <string, int> indices;

    double getPrice(int);
    double getPrice(string);
    double operator[](int);
    double operator[](string);

    int add(string, string, double);
    void update(int, double);
    void update(string, double);
};



void GetPrices(PriceDataset&);
void AddRialPairs(PriceDataset&);
void ComposeAndPushOrders(PriceDataset);

double GetUSDTIRR();


int main() {
    // try {
    //     // Create an Redis object, which is movable but NOT copyable.
    //     auto redis = Redis("tcp://127.0.0.1:6379");

    //     // ***** STRING commands *****

    //     redis.set("key", "val");
    //     auto val = redis.get("key");    // val is of type OptionalString. See 'API Reference' section for details.
    //     if (val) {
    //         // Dereference val to get the returned value of std::string type.
    //         std::cout << *val << std::endl;
    //     }   // else key doesn't exist.

    // } catch (const Error &e) {
    //     // Error handling.
    // }
    PriceDataset pd;
    GetPrices(pd);
    AddRialPairs(pd);

    for (auto p: pd.dataset)
        cout << p->symbol << ' ' << p->base << ' ' << p->id << ' ' << p->value << endl;

    // ComposeAndPushOrders(pd);
}

void GetPrices(PriceDataset &pd) {
    pd.add("BTC", "USDT", 34000);
}

void AddRialPairs(PriceDataset &pd) {
    double rate = GetUSDTIRR();
    for (auto p: pd.dataset)
        if (p->base == "USDT") {
            double new_rate = rate * p->value;
            pd.add(p->symbol, "IRR", new_rate);
        }
}

double GetUSDTIRR() {
    return 26000;
}

void Price::update_value(double new_value) {
    value = new_value;
}

void Price::update_symbol(string new_symbol) {
    symbol = new_symbol;
}

double PriceDataset::getPrice(int id) {
    return dataset[id]->value;
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

int PriceDataset::add(string name, string base, double price_value) {
    int new_id = dataset.size();
    Price *data = new Price(new_id, name, base, price_value);
    dataset.push_back(data);
    indices[name + base] = new_id;
    return new_id;
}

void PriceDataset::update(int id, double new_price) {
    dataset[id]->update_value(new_price);
}

void PriceDataset::update(string name, double new_price) {
    int id = indices[name];
    update(id, new_price);
}

