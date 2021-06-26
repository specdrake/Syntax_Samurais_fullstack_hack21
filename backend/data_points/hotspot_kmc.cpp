#include <bits/stdc++.h>
#include "helpers/calc.hpp"

#define ll long long

using namespace std;

int n;
vector<pt> points;
vector<pt> hotspots;

const int m = 50;

void input() {
    cin >> n;
    points.resize(n);
    for (int i = 0; i < n; ++i) {
        cin >> points[i].x >> points[i].y;
        points[i].c = -1;
    }
}

void initHS() {
    for (int i = 0; i < n; ++i) {
        int best = 0;
        float d = sqD(points[i], hotspots[0]);
        for (int j = 1; j < m; ++j) {
            float n_d = sqD(points[i], hotspots[j]);
            if (n_d < d) {
                d = n_d;
                best = j;
            }
        }
        points[i].c = best;
    }
}

void solve(bool final) {
    vector<pt> new_pts(m, {0,0,-1});
    vector<int> counts(m, 0);
    for (int i = 0; i < n; ++i) {
        new_pts[points[i].c].x += points[i].x;
        new_pts[points[i].c].y += points[i].y;
        counts[points[i].c] += 1;
    }

    for (int i = 0; i < m; ++i) {
        if (counts[i] == 0) continue;
        hotspots[i].x = new_pts[i].x / (float)counts[i];
        hotspots[i].y = new_pts[i].y / (float)counts[i];
    }

    if (final) return;
    bool new_found = false;

    for (int i = 0; i < n; ++i) {
        int prev = points[i].c;
        pair<int, float> best = {0, sqD(points[i], hotspots[0])};
        for (int j = 1; j < m; ++j) {
            float n_d = sqD(points[i], hotspots[j]);
            if (n_d < best.second)
                best = {j, n_d};
        }
        points[i].c = best.first;
        if (best.first != prev) new_found = true;
    }
    solve(!new_found);
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    srand(1);
    input();
    for (int i = 0; i < m; ++i) hotspots.push_back(getPt());
    initHS();
    solve(false);
    write("hotspots", hotspots);
    return 0;
}