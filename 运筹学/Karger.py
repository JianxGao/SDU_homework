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
    plt.figure(figsize=(5,3), dpi=300)
    pos = nx.kamada_kawai_layout(G)
    options = {
        "width": 0.15,
        "font_size": 7,
        "node_size":100,
        "node_color":range(len(G.nodes)),
        "cmap": plt.cm.Wistia,
        "with_labels": True,
    }

    pos[82][0]-=0.1
    pos[82][1]-=0.1
    pos[83][0]+=0.1
    pos[83][1]+=0.1

    nx.draw(G,pos=pos, **options)
    # edge_labels = {}
    # edges = list(G.edges())
    # for edge in edges:
    #     edge_num = edges.count(edge)
    #     edge_labels[edge] = edge_num
    # pos = nx.kamada_kawai_layout(G)
    # nx.draw_networkx_edge_labels(
    #     G, pos, edge_labels=edge_labels,
    #     verticalalignment='center')
    plt.savefig('BenchmarkNetwork.png'.format(num))
    plt.show()
    plt.close('all')


def contraction_algorithm(G):
    while G.number_of_nodes() > 2:
        edges = list(G.edges())
        random_int = np.random.randint(0, len(edges))
        removed_edge = edges[random_int]
        G = nx.contracted_edge(G, removed_edge, self_loops=False)
    return len(G.edges)


@calcute_total_time
def karger_algorithm(G, iteration):
    reuslt_list = []
    for i in range(iteration):
        min_cut = contraction_algorithm(G)
        reuslt_list.append(min_cut)
    return reuslt_list


if __name__ == '__main__':
    np.random.seed(1)
    filename = "./data/BenchmarkNetwork.txt"
    edges = read_data(filename)
    vertices = get_vertices(filename)

    G = nx.MultiGraph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)

    iteration=10
    result = karger_algorithm(G, iteration)
    print('Iteration={}'.format(iteration))
    print(min(result))
    print(result)




