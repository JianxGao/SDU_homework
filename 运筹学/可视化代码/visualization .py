import networkx as nx
import matplotlib.pyplot as plt


def plot_Ggg(G, pos, options, num):
    # plt.figure(figsize=(3, 6.5), dpi=300)
    plt.figure(figsize=(4, 8), dpi=200)
    nx.draw(G, pos=pos, **options)
    edge_labels = {}
    edges = list(G.edges())
    for edge in edges:
        edge_num = edges.count(edge)
        edge_labels[edge] = edge_num
    # pos = nx.kamada_kawai_layout(G)

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=16,
        verticalalignment='center')
    plt.savefig('{}.png'.format(num))
    plt.show(orientation=u'vertical')
    plt.close('all')




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

def Merge(dict1, dict2):
    return(dict2.update(dict1))


filename = "./data/test1.txt"
edges = read_data(filename)
vertices = get_vertices(filename)

G = nx.MultiGraph()

G.add_nodes_from(vertices)
G.add_edges_from(edges)

plt.figure(figsize=(4, 8), dpi=200)

G1 = nx.subgraph(G,[1,2,3,4,5])
G2 = nx.subgraph(G,[6,7,8,9,10])
pos1 = nx.circular_layout(G1)
pos2 = nx.circular_layout(G2)

dis1 = pos1[1][0]-pos1[2][0]
pos1[1][0]-=2*dis1
dis2 = pos1[2][0]-pos1[3][0]
pos1[3][0]+=2*dis2
pos1[4][0]+=2*dis2

pos = {}
for key,value in pos1.items():
    value[0] +=2
    pos[key] = value
for key,value in pos2.items():
    pos[key] = value
for key,value in pos.items():
    pos[key][0],pos[key][1] = pos[key][1],pos[key][0]

options = {
    "width": 0.8,
    "font_size": 18,
    "node_size": 650,
    "node_color": [1,1,1,1,1,0,0,0,0,0],
    "cmap": plt.cm.Wistia,
    "with_labels": True,
}

nx.draw(G, pos=pos, **options)
plt.savefig('1.png')
plt.show()
plt.close('all')

G = nx.contracted_edge(G, (4,5), self_loops = False)
# print(G.nodes())
G1 = nx.subgraph(G,[1,2,3,4])
G2 = nx.subgraph(G,[6,7,8,9,10])
pos1 = nx.circular_layout(G1)
pos2 = nx.circular_layout(G2)

pos = {}
for key,value in pos1.items():
    value[0] +=3
    pos[key] = value
for key,value in pos2.items():
    pos[key] = value


for key,value in pos.items():
    pos[key][0],pos[key][1] = pos[key][1],pos[key][0]

dis1 = pos1[1][1]-pos1[2][1]
pos[1][1]-=2*dis1
dis2 = pos1[2][1]-pos1[3][1]
pos[3][1]+=2*dis2
pos[3][0]+=0.5
pos[4][1]+=0.5
options = {
    "width": 0.8,
    "font_size": 18,
    "node_size": 650,
    "node_color": [1,1,1,1,0,0,0,0,0],
    "cmap": plt.cm.Wistia,
    "with_labels": True,
}

plot_Ggg(G,pos,options,2)


G = nx.contracted_edge(G, (1,2), self_loops = False)

G1 = nx.subgraph(G,[1,3,4])
G2 = nx.subgraph(G,[6,7,8,9,10])
pos1 = nx.circular_layout(G1)
pos2 = nx.circular_layout(G2)

pos = {}
for key,value in pos1.items():
    value[0] +=4
    pos[key] = value
for key,value in pos2.items():
    pos[key] = value


for key,value in pos.items():
    pos[key][0],pos[key][1] = pos[key][1],pos[key][0]

dis1 = pos1[1][1]-pos1[3][1]
pos[1][1]=pos[1][1]-dis1-1.5
# dis2 = pos1[2][1]-pos1[3][1]
# pos[3][1]+=2*dis2
# pos[3][0]+=0.5
# pos[4][1]+=0.5
options = {
    "width": 0.8,
    "font_size": 18,
    "node_size": 650,
    "node_color": [1,1,1,0,0,0,0,0],
    "cmap": plt.cm.Wistia,
    "with_labels": True,
}

plot_Ggg(G,pos,options,3)



G = nx.contracted_edge(G, (8,9), self_loops = False)

G1 = nx.subgraph(G,[1,3,4])
G2 = nx.subgraph(G,[6,7,8,10])
pos1 = nx.circular_layout(G1)
pos2 = nx.circular_layout(G2)

pos = {}
for key,value in pos1.items():
    value[0] +=4
    pos[key] = value
for key,value in pos2.items():
    pos[key] = value


for key,value in pos.items():
    pos[key][0],pos[key][1] = pos[key][1],pos[key][0]

dis1 = pos1[1][1]-pos1[3][1]
pos[1][1]=pos[1][1]-2*dis1
pos[8][0]+=0.5
options = {
    "width": 0.8,
    "font_size": 18,
    "node_size": 650,
    "node_color": [1,1,1,0,0,0,0],
    "cmap": plt.cm.Wistia,
    "with_labels": True,
}

plot_Ggg(G,pos,options,4)

G = nx.contracted_edge(G, (8,10), self_loops = False)

G1 = nx.subgraph(G,[1,3,4])
G2 = nx.subgraph(G,[6,7,8])
pos1 = nx.circular_layout(G1)
pos2 = nx.circular_layout(G2)

pos = {}
for key,value in pos1.items():
    value[0] +=4
    pos[key] = value
for key,value in pos2.items():
    pos[key] = value


for key,value in pos.items():
    pos[key][0],pos[key][1] = pos[key][1],pos[key][0]

dis1 = pos1[1][1]-pos1[3][1]
pos[1][1]=pos[1][1]-2*dis1
# pos[8][0]+=0.5
options = {
    "width": 0.8,
    "font_size": 18,
    "node_size": 650,
    "node_color": [1,1,1,0,0,0],
    "cmap": plt.cm.Wistia,
    "with_labels": True,
}

plot_Ggg(G,pos,options,5)


G = nx.contracted_edge(G, (1,4), self_loops = False)

G1 = nx.subgraph(G,[1,3])
G2 = nx.subgraph(G,[6,7,8])
pos1 = nx.circular_layout(G1)
pos2 = nx.circular_layout(G2)

pos = {}
for key,value in pos1.items():
    value[0] +=5
    pos[key] = value
for key,value in pos2.items():
    pos[key] = value


for key,value in pos.items():
    pos[key][0],pos[key][1] = pos[key][1],pos[key][0]

dis1 = pos1[1][1]-pos1[3][1]
pos[1][1]=pos[1][1]-2*dis1
# pos[8][0]+=0.5
options = {
    "width": 0.8,
    "font_size": 18,
    "node_size": 650,
    "node_color": [1,1,0,0,0],
    "cmap": plt.cm.Wistia,
    "with_labels": True,
}

plot_Ggg(G,pos,options,6)

G = nx.contracted_edge(G, (7,8), self_loops = False)

G1 = nx.subgraph(G,[1,3])
G2 = nx.subgraph(G,[6,7])
pos1 = nx.circular_layout(G1)
pos2 = nx.circular_layout(G2)

pos = {}
for key,value in pos1.items():
    value[0] +=5
    pos[key] = value
for key,value in pos2.items():
    pos[key] = value


for key,value in pos.items():
    pos[key][0],pos[key][1] = pos[key][1],pos[key][0]

dis1 = pos1[1][1]-pos1[3][1]
pos[1][1]=pos[1][1]-dis1-1.75
# pos[8][0]+=0.5
options = {
    "width": 0.8,
    "font_size": 18,
    "node_size": 650,
    "node_color": [1,1,0,0],
    "cmap": plt.cm.Wistia,
    "with_labels": True,
}

plot_Ggg(G,pos,options,7)

G = nx.contracted_edge(G, (1,3), self_loops = False)

G1 = nx.subgraph(G,[1])
G2 = nx.subgraph(G,[6,7])
pos1 = nx.circular_layout(G1)
pos2 = nx.circular_layout(G2)

pos = {}
for key,value in pos1.items():
    value[0] +=3
    pos[key] = value
for key,value in pos2.items():
    pos[key] = value


for key,value in pos.items():
    pos[key][0],pos[key][1] = pos[key][1],pos[key][0]


options = {
    "width": 0.8,
    "font_size": 18,
    "node_size": 650,
    "node_color": [1,0,0],
    "cmap": plt.cm.Wistia,
    "with_labels": True,
}

plot_Ggg(G,pos,options,8)


G = nx.contracted_edge(G, (6,7), self_loops = False)

G1 = nx.subgraph(G,[1])
G2 = nx.subgraph(G,[6])
pos1 = nx.circular_layout(G1)
pos2 = nx.circular_layout(G2)

pos = {}
for key,value in pos1.items():
    value[0] +=1
    pos[key] = value
for key,value in pos2.items():
    pos[key] = value


for key,value in pos.items():
    pos[key][0],pos[key][1] = pos[key][1],pos[key][0]


options = {
    "width": 0.8,
    "font_size": 18,
    "node_size": 650,
    "node_color": [1,0],
    "cmap": plt.cm.Wistia,
    "with_labels": True,
}

plot_Ggg(G,pos,options,9)