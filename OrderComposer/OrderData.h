#include <string>
#include <vector>

#include "PriceControllers.h"

using namespace std;

struct OrderTemplate {
    int type; // 0 for sell, 1 for buy
    double VolumeFraction, PriceMargin;

    OrderTemplate (string _t, double _vf, double _pm) {
        type = (_t == "Sell" or _t == "sell")? 0:1;
        PriceMargin = _pm; VolumeFraction = _vf;
    }

    bool is_buy();
    bool is_sell();
    string get_type();
    void push(long double, long double, string, string);
};

struct OrderPattern {
    vector <OrderTemplate> orders;
    double BaseBudget, AssetBudget;
    string AppliedBase, AppliedAsset;

    void read_budget();
    void make_standard();
    void generate_from_file();       // TODO
    void apply(string, string);
    void read_from_file(ifstream&);
    void push_orders(PriceDataset&);
};