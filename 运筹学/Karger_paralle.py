import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
from parelle import *


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
    fig, ax = plt.subplots(figsize=(8,6), dpi=200)
    options = {
        "ax":ax,
        "width": 0.2,
        "font_size": 8,
        "node_size":200,
        "node_color":range(len(G.nodes)),
        "cmap": plt.cm.GnBu,
        "with_labels": True,
    }
    nx.draw_kamada_kawai(G,**options)
    # nx.draw_networkx_edges()
    # plt.savefig('result/{}.png'.format(num))
    plt.show()


def Karger(G):
    while G.number_of_nodes() > 2:
        edges = list(G.edges())
        random_int = np.random.randint(0, len(edges))
        removed_edge = edges[random_int]
        G = nx.contracted_edge(G, removed_edge, self_loops = False)
    return len(list(G.edges()))


@calcute_total_time
def parallel_karger(G,n_processes):
    result = []
    threads = []
    for i in range(n_processes):
        t = My_Thread(Karger, args=(G,))
        threads.append(t)
    for i in range(n_processes):
        threads[i].start()
    for i in range(n_processes):
        threads[i].join()
    for i in range(n_processes):
        result.append(threads[i].get_result())
    return result


if __name__ == '__main__':
    filename = "./data/BenchmarkNetwork.txt"
    edges = read_data(filename)
    vertices = get_vertices(filename)
    G = nx.MultiGraph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    n_processes = 2
    result = parallel_karger(G,n_processes)
    print('The number of processes={}'.format(n_processes))
    print(result)
    print(min(result))

