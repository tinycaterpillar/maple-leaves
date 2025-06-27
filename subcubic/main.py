import sys
import networkx as nx
import matplotlib.pyplot as plt
from multiprocessing import Pool, Manager
import os

max_trials = 1000
num_processes = os.cpu_count() or 4
num_2 = 8  # 2의 개수 고정

def generate_and_check(index, shared_dict, degree_sequence):
    if shared_dict['done']:
        return

    G = nx.havel_hakimi_graph(degree_sequence)
    try:
        G_swapped = nx.double_edge_swap(G.copy(), nswap=100, max_tries=1000)
    except nx.NetworkXAlgorithmError:
        # 스왑 실패 시 원래 그래프 사용
        G_swapped = G

    if not nx.is_connected(G_swapped):
        return

    matching = nx.algorithms.matching.max_weight_matching(G_swapped, maxcardinality=True)
    if len(matching) * 2 != G_swapped.number_of_nodes():
        if not shared_dict['done']:
            shared_dict['done'] = True
            shared_dict['index'] = index
            shared_dict['graph'] = G_swapped
            shared_dict['matching'] = list(matching)

def run_experiment(degree_sequence):
    print(f"Running experiment for degree_sequence: {degree_sequence}")
    if not nx.is_graphical(degree_sequence):
        print("Error: Invalid degree sequence!")
        return

    with Manager() as manager:
        shared_dict = manager.dict()
        shared_dict['done'] = False

        with Pool(processes=num_processes) as pool:
            # degree_sequence 인자를 각 프로세스에 전달하려면 starmap 인자 구조 바꿔야 함
            args = [(i, shared_dict, degree_sequence) for i in range(max_trials)]
            pool.starmap(generate_and_check, args)

        if shared_dict.get('graph') is None:
            print("All Clear: Perfect matching found in all graphs.\n")
        else:
            G_result = shared_dict['graph']
            matching_edges = shared_dict['matching']
            pos = nx.spring_layout(G_result, seed=42)
            node_colors = ['skyblue' if G_result.degree(n) == 3 else 'lightgreen' for n in G_result.nodes()]

            plt.figure(figsize=(6, 6))
            nx.draw(G_result, pos, node_color=node_colors, node_size=500, with_labels=True)
            nx.draw_networkx_edges(G_result, pos, edgelist=matching_edges, edge_color='red', width=2)
            plt.title(f"Perfect Matching NOT Found (Trial {shared_dict['index'] + 1})\nDegree sequence: {degree_sequence}")
            plt.axis('off')
            plt.tight_layout()
            plt.show()
            sys.exit()

def main():
    for num_3 in range(2, 21, 2):  # 3의 개수를 2~10개까지 변경
        degree_sequence = [3] * num_3 + [2] * num_2
        degree_sequence.sort(reverse=True)  # Havel-Hakimi는 내림차순 권장
        run_experiment(degree_sequence)

if __name__ == "__main__":
    main()
