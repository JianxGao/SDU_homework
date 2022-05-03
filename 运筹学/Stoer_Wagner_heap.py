import networkx as nx
from itertools import islice
import time


def calculate_time(func):
    def wrapper(*args, **kargs):
        start_time = time.time()
        f = func(*args, **kargs)
        take_time = time.time() - start_time
        print()
        print()
        print("Function '{0}' takes {1:.3f}s.".format(
            func.__name__, take_time))
        return f
    return wrapper


class BHeap_dict(object):  # A Binary Heap
    def __init__(self):
        self.keys=[]
        self.values=[]

    def shift_up(self):
        insert_idx=len(self.values)-1
        parent_idx=(insert_idx-1)//2
        while insert_idx>0:
            if self.values[parent_idx]>=self.values[insert_idx]:
                break
            else:
                self.values[insert_idx],self.values[parent_idx]=\
                    self.values[parent_idx],self.values[insert_idx],
                self.keys[insert_idx], self.keys[parent_idx] = \
                    self.keys[parent_idx], self.keys[insert_idx],
                insert_idx=parent_idx
                parent_idx=(insert_idx-1)//2

    def shift_down(self,idx):
        current_idx=idx
        child_idx_left=current_idx*2+1
        child_idx_right=current_idx*2+2
        while current_idx<len(self.values)-1:
            if child_idx_left>len(self.values)-1:
                break
            elif child_idx_left==len(self.values)-1:
                if self.values[current_idx]>self.values[-1]:
                    break
                else:
                    self.values[current_idx],self.values[-1]=self.values[-1],self.values[current_idx]
                    self.keys[current_idx], self.keys[-1] = self.keys[-1], self.keys[current_idx]
                    break
            else:
                if self.values[current_idx]>max(self.values[child_idx_left],self.values[child_idx_right]):
                    break
                else:
                    if self.values[child_idx_right]>self.values[child_idx_left]:
                        self.values[child_idx_right],self.values[current_idx]=\
                            self.values[current_idx],self.values[child_idx_right]
                        self.keys[child_idx_right], self.keys[current_idx] = \
                            self.keys[current_idx], self.keys[child_idx_right]
                        current_idx=child_idx_right
                        child_idx_left = current_idx * 2 + 1
                        child_idx_right = current_idx * 2 + 2
                    else:
                        self.values[child_idx_left], self.values[current_idx]=\
                            self.values[current_idx], self.values[child_idx_left]
                        self.keys[child_idx_left], self.keys[current_idx] = \
                            self.keys[current_idx], self.keys[child_idx_left]
                        current_idx = child_idx_right
                        child_idx_left = current_idx * 2 + 1
                        child_idx_right = current_idx * 2 + 2

    def insert(self, key, value):
        if key not in self.keys:
            self.keys.append(key)
            self.values.append(value)
            self.shift_up()
        else:
            idx = self.keys.index(key)
            self.values[idx] += value

    def del_max(self):
        if len(self.keys)==0:
            print('Error!')
            raise NotImplementedError
        else:
            maxvalue=self.values.pop(0)
            maxkey=self.keys.pop(0)
            self.shift_down(0)
        return maxkey,maxvalue

    def findmax(self):
        return self.keys[0],self.values[0]

    def get(self,key):
        if key in self.keys:
            keyid=self.keys.index(key)
            value_got=self.values[keyid]
            return value_got
        else:
            return 0


@calculate_time
def stoer_wagner(G):
    nodes = set(G)
    merge=[]
    optimal=1e+9
    list_nodes=list(G.nodes)
    n=len(list_nodes)  # Num of nodes
    v0=list_nodes[0]  # Select v0 arbitrarily
    for i in range(n-1):
        A1=[v0]
        Maxheap=BHeap_dict()
        for v,e in G[v0].items():
            Maxheap.insert(v,e['weight'])
        for j in range(n-i-2):
            mkey,_=Maxheap.del_max()
            A1.append(mkey)
            for v,e in G[mkey].items():
                if v not in A1:
                    Maxheap.insert(v,e['weight'])
        last_key,maxv=Maxheap.findmax()
        if maxv<optimal:
            epoch=i
            optimal=maxv
        merge.append((mkey,last_key))
        for v1,e1 in G[last_key].items():
            if v1!=mkey:
                if v1 not in G[mkey]:
                    G.add_edge(mkey,v1,weight=e1['weight'])
                else:
                    G[mkey][v1]['weight']+=e1['weight']
        G.remove_node(last_key)
    G = nx.Graph(islice(merge, epoch))
    v = merge[epoch][1]
    G.add_node(v)
    reachable = set(nx.single_source_shortest_path_length(G, v))
    partition = (list(reachable), list(nodes - reachable))
    return optimal, partition


print('Please wait......')
G = nx.Graph()
with open('test1.txt', "r") as f:
    s = f.read()
# with open('BenchmarkNetwork.txt', "r") as f:
#     s = f.read()
# with open('Corruption_Gcc.txt', "r") as f:
#     s = f.read()
# with open('Crime_Gcc.txt', "r") as f:
#     s = f.read()
# with open('PPI_gcc.txt', "r") as f:
#     s = f.read()
# with open('RodeEU_gcc.txt', "r") as f:
#     s = f.read()
st=s.split('\n')
all_relation=[]
for item in st:
    all_relation.append(item.split(' '))
all_relation.pop(-1)
for item in all_relation:
    G.add_edge(str(item[0]),str(item[1]),weight=1)
cut_value, partition = stoer_wagner(G)
print(cut_value)
print(partition)
