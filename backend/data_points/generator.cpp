#include <bits/stdc++.h>
#include "helpers/calc.hpp"

#define ll long long

using namespace std;

const int n = 100'000;
const int m = 50;
vector<pt> points;
vector<pt> hotspots;

pt adjust(pt p) {
    pt nearest = hotspots[0];
    float d = sqD(p, nearest);
    for (int i = 1; i < m; ++i) {
        float n_d = sqD(p, hotspots[i]);
        if (n_d < d) {
            nearest = hotspots[i];
            d = n_d;
        }
    }
    float tr = rand() % 100;
    tr = tr * tr / 100.0;
    tr = 100.0 - tr;
    pt newpoint = {
        (nearest.x * tr + p.x * ((float)100-tr)) / (float)100,
        (nearest.y * tr + p.y * ((float)100-tr)) / (float)100
    };
    return newpoint;
}

int main(int argc, char** args) {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    int x;
    if(argc == 2)
        x = stoi(args[1]);
    else
        x = 0;
    srand(x);
    for (int i = 0; i < m; ++i) hotspots.push_back(getPt());
    for (int i = 0; i < n; ++i) points.push_back(adjust(getPt()));
    write("data", points);
    return 0;
}