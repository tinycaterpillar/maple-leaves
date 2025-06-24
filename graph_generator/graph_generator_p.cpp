// Build command: g++ -std=c++17 -fopenmp -O2 -mconsole graph_generator_p.cpp -o graph_generator_p
// Run command: ./graph_generator_p

#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <numeric>
#include <cassert>
#include <omp.h> // OpenMP 헤더

using namespace std;
using Edge = pair<int, int>;

vector<Edge> havel_hakimi_graph(vector<int> deg) {
    int n = deg.size();
    vector<int> label(n);
    iota(label.begin(), label.end(), 0);

    vector<Edge> edges;

    while (true) {
        vector<pair<int, int>> paired(n);
        for (int i = 0; i < n; ++i)
            paired[i] = {deg[i], label[i]};

        sort(paired.rbegin(), paired.rend());

        if (paired[0].first == 0)
            break;

        int d = paired[0].first;
        int u = paired[0].second;

        if (d > n - 1)
            throw runtime_error("Invalid degree sequence: degree too large");

        for (int i = 1; i <= d; ++i) {
            int v_deg = paired[i].first;
            int v = paired[i].second;

            if (v_deg == 0)
                throw runtime_error("Invalid degree sequence: not enough available vertices");

            edges.emplace_back(u, v);
            paired[i].first -= 1;
        }

        paired[0].first = 0;

        for (int i = 0; i < n; ++i) {
            deg[i] = paired[i].first;
            label[i] = paired[i].second;
        }
    }

    return edges;
}

int main() {
    ifstream infile("data/seq.txt");
    if (!infile) {
        cerr << "Error: Cannot open seq.txt\n";
        return 1;
    }

    string line;
    int num_of_vertices = -1;
    vector<string> lines;

    // 첫 줄에서 정점 수 읽기
    if (getline(infile, line)) {
        stringstream ss(line);
        ss >> num_of_vertices;
        if (num_of_vertices <= 0) {
            cerr << "Invalid vertex count\n";
            return 1;
        }
    }

    // 나머지 줄 저장
    while (getline(infile, line)) {
        lines.push_back(line);
    }
    infile.close();

    // 병렬 처리 시작
    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < (int)lines.size(); ++i) {
        stringstream ss(lines[i]);
        vector<int> deg;
        int d;
        while (ss >> d)
            deg.push_back(d);

        if ((int)deg.size() != num_of_vertices) {
            #pragma omp critical
            cerr << "Line " << i << ": invalid degree sequence length\n";
            continue;
        }

        try {
            auto edges = havel_hakimi_graph(deg);
            string filename = "data/graph_" + to_string(i) + ".txt";
            ofstream outfile(filename);
            outfile << num_of_vertices << "\n";
            for (auto [u, v] : edges) {
                outfile << u << " " << v << "\n";
            }
            outfile << lines[i] << "\n";
            outfile.close();

            #pragma omp critical
            cout << "Saved: " << filename << "\n";
        } catch (const exception& e) {
            #pragma omp critical
            cerr << "Error on line " << i << ": " << e.what() << "\n";
        }
    }

    return 0;
}
