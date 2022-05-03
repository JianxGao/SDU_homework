def plot_g(G, num):
    plt.figure(figsize=(5,3), dpi=400)
    pos = nx.kamada_kawai_layout(G)
    pos = nx.rescale_layout_dict(pos,scale=3)
    options = {
        "width": 0.1,
        "font_size": 2,
        "node_size":15,
        "node_color":range(len(G.nodes)),
        "cmap": plt.cm.Wistia,
        "with_labels": True,
    }

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
    plt.savefig('Crime_Gcc.png'.format(num))
    plt.show()
    plt.close('all')