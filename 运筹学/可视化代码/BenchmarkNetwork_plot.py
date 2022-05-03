
def plot_g(G, num):
    plt.figure(figsize=(5,3), dpi=600)
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
    #
    # nx.draw_networkx_edge_labels(
    #     G,
    #     pos,
    #     edge_labels=edge_labels,
    #     verticalalignment='center')
    plt.savefig('BenchmarkNetwork.png'.format(num))
    plt.show()
    plt.close('all')
    # print(num)