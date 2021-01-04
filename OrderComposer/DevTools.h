#include <chrono>
#include <ctime>

using namespace std;
typedef chrono::steady_clock::time_point _timer;

_timer devnow();

void devdiff(_timer s, _timer e = devnow());