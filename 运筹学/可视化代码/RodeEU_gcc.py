def plot_g(G, num):
    plt.figure(figsize=(5,3), dpi=400)
    pos = nx.kamada_kawai_layout(G)
    pos = nx.rescale_layout_dict(pos,scale=3)

    options = {
        "width": 0.1,
        "font_size": 2,
        "node_size": 15,
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
    plt.savefig('RodeEU_gcc.png'.format(num))
    foo_fig = plt.gcf()  # 'get current figure'
    foo_fig.savefig('foo.eps', format='eps', dpi=1000)
    plt.show()
    plt.close('all')


def plot_g(G, num):
    plt.figure(figsize=(10,6.18), dpi=600)
    pos = nx.kamada_kawai_layout(G)
    pos = nx.rescale_layout_dict(pos,scale=3)

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
    plt.savefig('RodeEU_gcc.png'.format(num))
    # foo_fig = plt.gcf()
    # foo_fig.savefig('RodeEU_gcc.eps', format='eps', dpi=1000)
    plt.show()
    plt.close('all')