#include <bits/stdc++.h>

using namespace std;

struct pt {
    float x, y;
    int c;
};

const float vlb = 28.7, vub = 28.783, hlb = 77.033, hub = 77.177;
const float vs = vub - vlb, hs = hub - hlb;

float sqD(pt a, pt b) {
    return (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y);
}

pt getPt() {
    int h = rand();
    int v = rand();
    int up = v % (int)(vs * 1e4);
    int ri = h % (int)(hs * 1e4);
    return {hlb + ri / (float)(1e4), vlb + up / (float)(1e4), -1};
}

void write(string fname, vector<pt> points) {
    int n = points.size();
    ofstream f1;
    f1.open(fname);
    f1 << n << endl;
    for (int i = 0; i < n; ++i) {
        f1 << points[i].x << " " << points[i].y << endl;
    }
}