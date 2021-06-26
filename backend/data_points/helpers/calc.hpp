#include <bits/stdc++.h>
struct pt {
    float x, y;
    int c;
};
static const float vlb = 28.7, vub = 28.783, hlb = 77.033, hub = 77.177;
static const float vs = vub - vlb, hs = hub - hlb;
float sqD(pt, pt);
pt getPt();
void write(std::string, std::vector<pt>);