def plot_g(G, num):
    plt.figure(figsize=(10,6.18), dpi=450)
    pos = nx.kamada_kawai_layout(G)
    pos = nx.rescale_layout_dict(pos,scale=2)

    options = {
        "width": 0.1,
        "font_size": 5,
        "node_size": 70,
        "node_color":range(len(G.nodes)),
        "cmap": plt.cm.Wistia,
        "with_labels": True,
    }

    nx.draw(G, pos=pos, **options)
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
    plt.savefig('PPI_gcc.png'.format(num))
    plt.show()
    plt.close('all')