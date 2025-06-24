// Build command: g++ -std=c++17 -fopenmp -O2 -mconsole degree_sequences_p.cpp -o degree_sequences_p
// Run command: ./degree_sequences_p

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cassert>
#include <chrono>
#include <mutex>
#include <omp.h>

#define endl "\n"
#define all(v) (v).begin(), (v).end()

using namespace std;

int NUM_OF_V;
int TOTAL_DEG, TOTAL_EDGE;
int SEQ_NUM = 0;
mutex output_mutex;
ofstream outfile("data/seq.txt");

// 1-indexed Fenwick Tree
template <class T>
struct Fenwick {
    int n;
    vector<T> fw;
    Fenwick() = default;
    Fenwick(int n) : n{n}, fw(n + 1, T{}) {}
    void update(int ind, T delta) {
        while (ind <= n) {
            fw[ind] += delta;
            ind += (ind & -ind);
        }
    }
    T get(int ind) {
        T ret{};
        while (ind > 0) {
            ret += fw[ind];
            ind -= (ind & -ind);
        }
        return ret;
    }
};

bool deg_symmetry(vector<int>& deg) {
    for (int i = 1; i <= NUM_OF_V; ++i) {
        if (deg[i] + deg[NUM_OF_V + 1 - i] != NUM_OF_V - 1) return false;
    }
    return true;
}

bool Erdos_Gallai(vector<int>& deg, Fenwick<int>& acc, int odd) {
    if (odd & 1) return false;
    for (int k = 1; k <= NUM_OF_V; ++k) {
        int left = acc.get(k);
        int right = k * (k - 1);
        auto p = upper_bound(deg.begin(), deg.end(), k,
            [](int a, int b) { return a > b; }) - deg.begin();
        if (p < k + 1) {
            right += acc.get(NUM_OF_V) - acc.get(k);
        } else if (p <= NUM_OF_V) {
            right += (p - k - 1) * k;
            right += acc.get(NUM_OF_V) - acc.get(p - 1);
        } else {
            right += (NUM_OF_V - k) * k;
        }
        if (left > right) return false;
    }
    return true;
}

void partition(vector<int>& deg, Fenwick<int>& acc, int ind, int rm_deg, int sum, int odd) {
    if (ind > NUM_OF_V) {
        if (!deg_symmetry(deg)) return;
        if (!Erdos_Gallai(deg, acc, odd)) return;

        // ✅ thread-safe 출력 구간
        {
            lock_guard<mutex> lock(output_mutex);
            for (int i = 1; i <= NUM_OF_V; ++i) outfile << deg[i] << " ";
            outfile << endl;
            SEQ_NUM += 1;
        }
        return;
    }

    for (int d = min(rm_deg, deg.back()); d >= 0; --d) {
        deg.push_back(d);
        odd += (d & 1);
        acc.update(ind, d);
        if (sum + (NUM_OF_V - ind + 1) * d >= TOTAL_DEG) {
            partition(deg, acc, ind + 1, rm_deg - d, sum + d, odd);
        }
        deg.pop_back();
        odd -= (d & 1);
        acc.update(ind, -d);
        if (sum + (NUM_OF_V - ind + 1) * d < TOTAL_DEG) break; // pruning
    }
}

int main() {
    using namespace std::chrono;
    auto start = high_resolution_clock::now();

    cin >> NUM_OF_V;
    assert(NUM_OF_V % 4 == 0 || NUM_OF_V % 4 == 1);
    assert(NUM_OF_V < 10000); // overflow 방지

    outfile << NUM_OF_V << endl;
    TOTAL_DEG = NUM_OF_V * (NUM_OF_V - 1) / 2;
    TOTAL_EDGE = TOTAL_DEG / 2;

    #pragma omp parallel for schedule(dynamic)
    for (int d = NUM_OF_V - 1; d >= 0; --d) {
        vector<int> deg;
        deg.push_back(NUM_OF_V - 1); // dummy
        deg.push_back(d);

        Fenwick<int> acc(NUM_OF_V);
        acc.update(1, d);
        int sum = d;
        int odd = (d & 1);

        partition(deg, acc, 2, TOTAL_DEG - d, sum, odd);
    }

    outfile.close();

    auto end = high_resolution_clock::now();
    duration<double> elapsed = end - start;
    cout << "Elapsed time: " << elapsed.count() << " seconds" << endl;
    cout << "Total sequences: " << SEQ_NUM << endl;

    return 0;
}
