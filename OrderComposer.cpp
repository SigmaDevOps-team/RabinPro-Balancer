#include <iostream>

using namespace std;

class Price {
    private:
        string symbol;
        int id;
        double value;
    
    public:
        Price(int _id, string _symbol, double _value) {
            id = _id; symbol = _symbol; value = _value;
        }

        void update_value(double);
        void update_symbol(string); 
}

class PriceDataset {
    private:
        vector <*Price> dataset;
        map <string, int> indices;

    public:
        double getPrice(int);
        double getPrice(string);
        double operator[](int);
        double operator[](string);

        int add(string, double);
        void update(int, double);
        void update(string, double);
}

void GetPrices();
void Convert2Rial();
void ComposerAndPushOrders();

int main() {
    GetPrices();
    Convert2Rial();
    ComposeAndPushOrders();
}

void GetPrices() {

}

void Convert2Rial() {

}

void ComposeAndPushOrders() {

}

void Price::update_value(double new_value) {
    value = new_value;
}

void Price::update_symbol(string new_symbol) {
    symbol = new_symbol;
}

double PriceDataset::getPrice(int id) {
    return dataset[id].value;
}

double PriceDataset::getPrice(string name) {
    id = indices[name];
    return getPrice(id);
}

double PriceDataset::operator[](int id) {
    return getPrice(id);
}

double PriceDataset::operator[](string name) {
    return getPrices(name);
}

int PriceDataset::add(string name, double price_value) {
    int new_id = dataset.size();
    Price data = new Price(new_id, name, price_value);
    dataset.push_back(&data);
    indices[name] = new_id;
}

void PriceDataset::update(int id, double new_price) {
    dataset[id]->update_value(new_price);
}

void PriceDataset::update(string name, double new_price) {
    int id = indices[name];
    update(id, new_price);
}

