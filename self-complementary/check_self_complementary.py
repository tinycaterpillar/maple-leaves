import networkx as nx
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed

# --------- 설정 ---------
max_trials = 1000
num_workers = 8
data_path = "data/seq.txt"
# -------------------------

def is_non_self_complementary_once(degree_sequence):
    G = nx.havel_hakimi_graph(degree_sequence)
    try:
        G = nx.double_edge_swap(G.copy(), nswap=100, max_tries=1000)
    except nx.NetworkXAlgorithmError:
        pass

    Gc = nx.complement(G)
    return not nx.is_isomorphic(G, Gc), G, Gc

def test_one_sequence(seq_info):
    index, degree_sequence = seq_info
    for trial in range(max_trials):
        fail, G, Gc = is_non_self_complementary_once(degree_sequence)
        if fail:
            return {
                'index': index,
                'sequence': degree_sequence,
                'trial': trial,
                'graph': G,
                'complement': Gc
            }
    return None

def visualize_failure(result):
    G = result['graph']
    Gc = result['complement']
    
    # 동일한 노드 위치를 양쪽 그래프에 사용
    # pos = nx.spring_layout(G, seed=42) # use this if kamada_kawai_layout is too slow
    G_pos = nx.kamada_kawai_layout(G)
    Gc_pos = nx.kamada_kawai_layout(Gc)

    plt.figure(figsize=(14, 6))

    # 원래 그래프
    plt.subplot(1, 2, 1)
    nx.draw_networkx_nodes(G, G_pos, node_color='skyblue', node_size=800)
    nx.draw_networkx_edges(G, G_pos, edge_color='gray', width=1.5)
    nx.draw_networkx_labels(G, G_pos, font_size=10)
    plt.title(f"G (Trial {result['trial'] + 1})")
    plt.axis('off')

    # 컴플리먼트 그래프
    plt.subplot(1, 2, 2)
    nx.draw_networkx_nodes(Gc, Gc_pos, node_color='salmon', node_size=800)
    nx.draw_networkx_edges(Gc, Gc_pos, edge_color='gray', width=1.5)
    nx.draw_networkx_labels(Gc, Gc_pos, font_size=10)
    plt.title("Complement of G")
    plt.axis('off')

    plt.suptitle(f"Sequence #{result['index']} is NOT self-complementary", fontsize=14)
    plt.show()

    
def load_sequences(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    sequences = []
    for line in lines:
        tokens = line.strip().split()
        if not tokens or len(tokens) == 1: continue
        sequences.append(list(map(int, tokens)))
    return sequences

def main():
    sequences = load_sequences(data_path)
    print(f"Loaded {len(sequences)} sequences.")

    indexed_seqs = list(enumerate(sequences, start=1))

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(test_one_sequence, seq_info) for seq_info in indexed_seqs]
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(f"\nSequence #{result['index']} failed self-complementarity!")
                print(f"→ Degree sequence: {result['sequence']}")
                visualize_failure(result)
                return

    print("\nAll sequences passed. All generated graphs were self-complementary.")

if __name__ == "__main__":
    main()
