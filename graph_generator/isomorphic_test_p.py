import os
from collections import Counter
import networkx as nx
from networkx.algorithms import isomorphism as iso
from concurrent.futures import ProcessPoolExecutor, as_completed

def load_graph_from_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.read().strip().splitlines()

    n = int(lines[0])
    num_edges = n * (n - 1) // 4
    edge_lines = lines[1:1 + num_edges]
    degree_seq_line = lines[-1]

    G = nx.Graph()
    G.add_nodes_from(range(n))
    for line in edge_lines:
        u, v = map(int, line.split())
        G.add_edge(u, v)

    return G, degree_seq_line

def extract_index(filename, prefix):
    return int(filename[len(prefix):-4])

def has_odd_frequency(nums):
    freq = Counter(nums)
    return any(count % 2 == 1 for count in freq.values())

def check_isomorphism(idx, graph_path, complement_path):
    G1, deg_seq1 = load_graph_from_file(graph_path)
    G2, _ = load_graph_from_file(complement_path)

    if G1.number_of_nodes() != G2.number_of_nodes():
        return f"✘ graph_{idx} and complement_{idx} are NOT isomorphic (vertex count mismatch)", deg_seq1, False

    gm = iso.GraphMatcher(G1, G2)
    warn = has_odd_frequency(deg_seq1.split())
    if gm.is_isomorphic():
        return f"✔ graph_{idx} and complement_{idx} are isomorphic", deg_seq1, warn
    else:
        return f"✘ graph_{idx} and complement_{idx} are NOT isomorphic", deg_seq1, warn

def main():
    data_dir = "data"
    if not os.path.exists(data_dir):
        print("Directory 'data' not found.")
        return

    graph_files = {}
    complement_files = {}

    for name in os.listdir(data_dir):
        if name.startswith("graph_") and name.endswith(".txt"):
            idx = extract_index(name, "graph_")
            graph_files[idx] = os.path.join(data_dir, name)
        elif name.startswith("complement_") and name.endswith(".txt"):
            idx = extract_index(name, "complement_")
            complement_files[idx] = os.path.join(data_dir, name)

    tasks = []
    results = []
    with ProcessPoolExecutor() as executor:
        for idx in sorted(graph_files):
            if idx not in complement_files:
                print(f"✘ complement_{idx}.txt not found")
                continue
            tasks.append(executor.submit(check_isomorphism, idx, graph_files[idx], complement_files[idx]))

        for future in as_completed(tasks):
            result, deg_seq, warn = future.result()
            output = result + "\n"
            output += f"data seq: {deg_seq}\n"
            if result:
                print(result)
                print(f"data seq: {deg_seq}")
                if warn:
                    print("⚠️ degree sequence에 홀수 번 등장한 수가 있습니다.")
                print()
            output += "\n"
            results.append(output)
    
    with open("result.txt", "w", encoding="utf-8") as f:
        f.writelines(results)

if __name__ == "__main__":
    main()
