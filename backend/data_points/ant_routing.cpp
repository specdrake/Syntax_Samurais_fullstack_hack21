#include <bits/stdc++.h>
#include "helpers/calc.hpp"

#define ll long long

using namespace std;

int n;
vector<pt> points;

const int m = 50;
const int num_ants = 10;
const float distPower = 2.0, pheromonePower = 7.0;

vector<vector<float>> dists(m, vector<float>(m, 0));
vector<vector<float>> phers(m, vector<float>(m, 1));
vector<pt> best_path_so_far;
float best_dist = 1e9;

vector<int> dfs(int s, vector<bool> trav, vector<int> path) {
    trav[s] = true;
    path.emplace_back(s);
    vector<pair<int, float>> probs;
    float tot = 0;
    for (int i = 0; i < m; ++i) {
        if (trav[i]) continue;
        float ncp = pow(1 / dists[s][i], distPower) * pow(phers[s][i], pheromonePower);
        tot += ncp;
        probs.push_back({i, tot});
    }
    if (probs.size() == 0) return path;
    float prob = fmod(rand() * 1e-4, 1);
    int chosen;
    for (int i = 0; i < probs.size(); ++i) {
        probs[i].second /= tot;
        if (probs[i].second >= prob) {
            chosen = probs[i].first;
            break;
        }
    }
    return dfs(chosen, trav, path);
}

vector<int> bpdfs(int s, vector<bool> trav, vector<int> path) {
    trav[s] = true;
    path.emplace_back(s);
    float best = 1e9;
    float best_str = -1e9;
    for (int i = 0; i < m; ++i) {
        if (trav[i]) continue;
        if (best == 1e9 || best < phers[s][i]) {
            best_str = phers[s][i];
            best = i;
        } 
    }
    if (best == 1e9) return path;
    return dfs(best, trav, path);
}

void eval(vector<pt> path) {
    float d = sqD(path[0], path[m-1]);
    for (int i = 1; i < m; ++i) {
        d += sqD(path[i], path[i-1]);
    }
    if (d < best_dist) {
        best_dist = d;
        best_path_so_far = path;
    }
}

vector<pt> getTrail() {
    vector<bool> trav(m, false);
    vector<int> best_path = bpdfs(0, trav, vector<int>());
    vector<pt> fin_path;
    for (int i = 0; i < m; ++i) {
        fin_path.push_back(points[best_path[i]]);
    }
    return fin_path;
}

void input() {
    cin >> n;
    points.resize(n);
    for (int i = 0; i < n; ++i) {
        cin >> points[i].x >> points[i].y;
        points[i].c = -1;
    }
    eval(points);
}

void initMats() {
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            float s = sqD(points[i], points[j]);
            dists[i][j] = s;
            dists[j][i] = s;
        }
    }
}

bool cmp(pair<float, int> a, pair<float, int> b) {
    return a.first < b.first;
}

void solve() {
    // place ants at random points
    set<int> start;
    while (start.size() < num_ants) {
        int x = rand() % m;
        start.insert(x);
    }

    vector<int> ant_starts;

    for (auto it: start) {
        ant_starts.emplace_back(it);
    }

    vector<vector<int>> ant_paths;

    for (int i = 0; i < num_ants; ++i) {
        ant_paths.push_back(dfs(ant_starts[i], vector<bool>(m, false), vector<int>()));
    }

    // Rate all paths based on length
    vector<pair<float, int>> dists;
    for (int i = 0; i < num_ants; ++i) {
        float d = sqD(points[ant_paths[i][0]], points[ant_paths[i][m-1]]);
        for (int j = 1; j < m; ++j) {
            d += sqD(points[ant_paths[i][j]], points[ant_paths[i][j-1]]);
        }
        dists.push_back({d, i});
    }
    
    // Recalculate Pheromone Strengths
    phers = vector<vector<float>>(m, vector<float>(m, 0.1));

    sort(dists.begin(), dists.end(), cmp);
    for (int i = 0; i < num_ants; ++i) {
        // cout << dists[i].first << " " << dists[i].second << endl;
        for (int j = 1; j < ant_paths[i].size(); ++j) {
            phers[ant_paths[i][j]][ant_paths[i][j-1]] += (5 - i) * 1e-3 * 5;
            phers[ant_paths[i][j-1]][ant_paths[i][j]] += (5 - i) * 1e-3 * 5;
        }
        phers[ant_paths[i][0]][ant_paths[i][m-1]] += (5 - i) * 1e-3 * 5;
        phers[ant_paths[i][m-1]][ant_paths[i][0]] += (5 - i) * 1e-3 * 5;
    }
}


int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    srand(2);
    input();
    initMats();
    for (int i = 0; i < 100; ++i){
        solve();
        eval(getTrail());
    }
    write("van_path", best_path_so_far);
    return 0;
}