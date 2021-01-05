g++ -std=c++17 \
OrderComposer.cpp \
DevTools.cpp \
Components.cpp \
Constants.cpp \
PriceControllers.cpp \
redis-plus-plus/compile/lib/libredis++.a \
-lredis++ \
-lhiredis \
-pthread \
-o order-composer