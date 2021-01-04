#include <iostream>
#include <chrono>
#include <ctime>

using namespace std;
typedef chrono::steady_clock::time_point _timer;

_timer _snow()
{
    return chrono::steady_clock::now();
}
void _coutdiff(_timer s, _timer e = _snow())
{
    cout << "Time difference = ";
    cout << chrono::duration_cast<std::chrono::microseconds>(e - s).count();
    cout << "[µs] = ";
    cout << chrono::duration_cast<std::chrono::nanoseconds>(e - s).count();
    cout << "[ns]" << endl;
}