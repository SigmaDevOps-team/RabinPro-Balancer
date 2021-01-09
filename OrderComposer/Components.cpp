#include <iostream>
#include <string>

#include "Components.h"

using namespace std;

void found_exception(string status)
{
    cout << status << endl;
    exit(-1);
}