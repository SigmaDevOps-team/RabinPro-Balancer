#include <string>
#include <vector>
#include <fstream>

#include "OrderData.h"

bool OrderTemplate::is_sell() {
    return type == 0;
}

bool OrderTemplate::is_buy() {
    return !is_buy();
}

string OrderTemplate::get_type() {
    return is_sell()? "Sell":"Buy";
}

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