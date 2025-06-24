#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cassert>

using namespace std;

using Edge = pair<int, int>;

// input: A valid deg sequece
// output: Edge list sadisfing given seq
vector<Edge> havel_hakimi_graph(vector<int> deg) {
    int n = deg.size();
    vector<int> label(n);  // V(G) = {0, 1, ... n-1}
    iota(label.begin(), label.end(), 0);

    vector<Edge> edges;

    while (true) {
        // deg, label 을 degree 기준으로 내림차순 정렬
        vector<pair<int, int>> paired(n);
        for (int i = 0; i < n; ++i)
            paired[i] = {deg[i], label[i]};

        sort(paired.rbegin(), paired.rend());

        // 모두 0이면 종료
        if (paired[0].first == 0)
            break;

        int d = paired[0].first;
        int u = paired[0].second;

        if (d > n - 1) {
            throw runtime_error("Invalid degree sequence: degree too large");
        }

        for (int i = 1; i <= d; ++i) {
            int v_deg = paired[i].first;
            int v = paired[i].second;

            if (v_deg == 0) {
                throw runtime_error("Invalid degree sequence: not enough available vertices");
            }

            edges.emplace_back(u, v);
            paired[i].first -= 1;
        }

        // 현재 정점의 차수는 0으로
        paired[0].first = 0;

        // deg, label 업데이트
        for (int i = 0; i < n; ++i) {
            deg[i] = paired[i].first;
            label[i] = paired[i].second;
        }
    }

    return edges;
}

int main() {
    vector<int> deg{6, 5, 5, 4, 3, 2, 2, 1};
    cout << "deg seq: ";
    for(auto e: deg) cout << e << ' ' ;
    cout << endl; 

    auto edge = havel_hakimi_graph(deg);
    for(auto e: edge){
        cout << e.first << ' ' << e.second << endl;
    }

    return 0;
}