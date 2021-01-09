#include <vector>
#include <map>
#include <string>

using namespace std;

struct Price
{
    int id;
    double value;
    int cache_usage;
    string name, base;

    Price(int _id, string _name, string _base)
    {
        id = _id;
        name = _name;
        base = _base;
        cache_usage = 100;
        value = -1;
    }

    string symbol();
    double get_value();
    void update_symbol(string, string);
};


struct PriceDataset
{
    vector<Price *> dataset;
    map<string, int> indices;

    double getPrice(int);
    double getPrice(string);
    double operator[](int);
    double operator[](string);

    int add(string, string);
    int add(pair<string, string>);
};
