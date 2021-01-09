#include <string>
#include <vector>

using namespace std;

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

struct OrderPattern {
    vector <OrderTemplate> orders;

    void read_from_file(ifstream&);
    void generate_from_file(); // TODO
    void make_standard();
};