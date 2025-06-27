#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <string>
#include <sstream>
#include <filesystem>
#include <algorithm>
#include <string>

namespace fs = std::filesystem;

void make_complement(const std::string& input_path, const std::string& output_path) {
    std::ifstream infile(input_path);
    if (!infile) {
        std::cerr << "Error: Cannot open " << input_path << "\n";
        return;
    }

    int n;  // 정점 수
    infile >> n;

    int num_edges = n * (n - 1) / 4;

    std::set<std::pair<int, int>> edge_set;
    int u, v;
    int max_vertex = -1;

    // 간선 개수만큼 정확히 읽음
    for (int i = 0; i < num_edges; ++i) {
        if (!(infile >> u >> v)) {
            std::cerr << "Error: Not enough edge lines in " << input_path << "\n";
            return;
        }
        if (u == v) continue;
        int a = std::min(u, v);
        int b = std::max(u, v);
        edge_set.insert({a, b});
        max_vertex = std::max({max_vertex, a, b});
    }
    infile.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::string seq;
    std::getline(infile, seq);
    infile.close();

    std::ofstream outfile(output_path);
    if (!outfile) {
        std::cerr << "Error: Cannot create " << output_path << "\n";
        return;
    }

    outfile << n << "\n";
    // 간선 개수 출력
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (edge_set.find({i, j}) == edge_set.end()) {
                outfile << i << " " << j << "\n";
            }
        }
    }
    outfile << seq << "\n";

    outfile.close();
    std::cout << "Complement saved to " << output_path << "\n";
}

bool starts_with(const std::string& str, const std::string& prefix) {
    return str.size() >= prefix.size() &&
           str.compare(0, prefix.size(), prefix) == 0;
}

bool ends_with(const std::string& str, const std::string& suffix) {
    return str.size() >= suffix.size() &&
           str.compare(str.size() - suffix.size(), suffix.size(), suffix) == 0;
}

int main() {
    const std::string dir = "data";
    if (!fs::exists(dir)) {
        std::cerr << "Error: Directory 'data' does not exist.\n";
        return 1;
    }

    for (const auto& entry : fs::directory_iterator(dir)) {
        std::string filename = entry.path().filename().string();
        if (starts_with(filename, "graph_") && ends_with(filename, ".txt")) {
            std::string index = filename.substr(6, filename.size() - 10); // "graph_" + idx + ".txt"
            std::string input_path = dir + "/" + filename;
            std::string output_path = dir + "/complement_" + index + ".txt";
            make_complement(input_path, output_path);
        }
    }

    return 0;
}
