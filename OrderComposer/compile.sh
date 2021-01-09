g++ -std=c++11 \
OrderComposer.cpp \
DevTools.cpp \
Components.cpp \
Constants.cpp \
PriceControllers.cpp \
OrderData.cpp \
redis-plus-plus/compile/lib/libredis++.a \
-lredis++ \
-lhiredis \
-pthread \
-o order-composer