import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time


def calcute_total_time(func):
    def code_wrapper(*args, **kargs):
        start_time = time.time()
        f = func(*args, **kargs)
        take_time = time.time() - start_time
        print("Function '{0}' takes {1:.3f}s.".format(
            func.__name__, take_time))
        return f
    return code_wrapper


def read_data(filename):
    dataset = []
    with open(filename) as f:
        for row in f:
            node = row.split()
            node = int(node[0]),int(node[1])
            dataset.append(node)
    return dataset


def get_vertices(filename):
    vertices = []
    with open(filename) as f:
        for row in f:
            node =  row.split()
            vertices.append(int(node[0]))
            vertices.append(int(node[1]))
    return list(set(vertices))


def plot_g(G, num):
    plt.figure(figsize=(8,6), dpi=200)
    options = {
        "width": 0.2,
        "font_size": 8,
        "node_size":200,
        "node_color":range(len(G.nodes)),
        "cmap": plt.cm.GnBu,
        "with_labels": True,
    }
    edge_labels = {}
    edges = list(G.edges())
    for edge in edges:
        edge_num = edges.count(edge)
        edge_labels[edge] = edge_num
    pos = nx.kamada_kawai_layout(G)
    nx.draw_kamada_kawai(G, **options)
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        verticalalignment='center')
    plt.savefig('RodeEU_gcc/{}.png'.format(num))
    plt.close('all')
    print(num)


def Karger_algorithm(G, t):
    # num = 0
    while G.number_of_nodes() > t:
        edges = list(G.edges())
        random_int = np.random.randint(0, len(edges))
        removed_edge = edges[random_int]
        G = nx.contracted_edge(G, removed_edge, self_loops=False)
        # num+=1
        # plot_g(G, num)
    return G


def trick2(G,L):
    V = G.number_of_nodes()
    if V <= 6:
        return len(list(Karger_algorithm(G, 2).edges()))
    else:
        t = int(1 + V / np.sqrt(2))
        G_all = []
        for i in range(L):
            G_all.append(Karger_algorithm(G, t))
        result = trick2(G_all[0], L)
        for i in range(1, L):
            result = min(result,trick2(G_all[i],L))
        return result


@calcute_total_time
def karger_stein_algorithm(G, L, iteration):
    reuslt_list = []
    for i in range(iteration):
        min_cut = trick2(G, L)
        reuslt_list.append(min_cut)
    return  reuslt_list


if __name__ == '__main__':
    np.random.seed(1)
    filename = "./data/BenchmarkNetwork.txt"
    edges = read_data(filename)
    vertices = get_vertices(filename)

    G = nx.MultiGraph()

    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    L = 3
    iteration = 1
    improved_result = karger_stein_algorithm(G, L, iteration)
    print('Iteration={}'.format(iteration))
    print(min(improved_result))
    print(improved_result)



