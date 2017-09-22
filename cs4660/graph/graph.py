from io import open
from builtins import range

class Node:
    def __init__(self, node_name):
        self.node_name = node_name

    def __eq__(self, other):
        return self.node_name==other.node_name

    def __hash__(self):
        return hash(self.node_name)
        
class Edge:
    def __init__(self, node1, node2, cost):
        self.node1 = node1
        self.node2 = node2
        self.cost = cost

    def __eq__(self, other):
        return self.node1==other.node1 and self.node2==other.node2 and self.cost==other.cost

    def __hash__(self):
        return hash(self.node1, self.node2)

def construct_graph_from_file(obj, file_path):
    f = open(file_path, encoding='utf-8')
    first_line = f.readline()
    for i in range(int(first_line)):
        obj.add_node(Node(i))
    text = f.read()
    lines = text.split('\n')
    for line in lines:
        if len(line) > 0:
            values = line.split(':')
            edge = Edge( Node( int( values[0] ) ), Node( int( values[1] ) ), int( values[2] ) )
            obj.add_edge(edge)
    return obj

class AdjacencyList:

    def __init__(self):
        self.nodes={}

    def add_node(self, node):
        if(node in self.nodes):
            return False
        self.nodes[node]={}
        return True

    def add_edge(self, edge):
        self.add_node(edge.node1)
        if(edge.node2 in self.nodes[edge.node1]):
            return False
        self.nodes[edge.node1][edge.node2]=edge
        return True

    def remove_edge(self, edge):
        if(edge.node1 in self.nodes and edge.node2 in self.nodes[edge.node1]):
            del self.nodes[edge.node1][edge.node2]
            return True
        return False
    
    def remove_node(self, node):
        if(node in self.nodes):
            del self.nodes[node]
            for n in self.nodes:
                self.remove_edge( Edge( n, node, 0 ) )
            return True
        return False

    def adjacent(self, node1, node2):
        if(node1 in self.nodes and node2 in self.nodes[node1]):
            return True
        return False
    
    def neighbors( self, node ):
        return [ k for k in self.nodes[node] ]

class AdjacencyMatrix:

    def __init__(self):
        self.nodes=[]

    def add_node(self, node):
        if(len(self.nodes)>node.node_name):
            return False
        self.nodes.append([])
        for i in range(len(self.nodes)):
            self.nodes[i].append(0)
        return True

    def add_edge(self, edge):
        if(len(self.nodes)>edge.node1.node_name and len(self.nodes[edge.node1.node_name])>edge.node2.node_name 
            and self.nodes[edge.node1.node_name][edge.node2.node_name]>0):
            return False
        self.nodes[edge.node1.node_name][edge.node2.node_name]=edge.cost
        return True

    def remove_edge(self, edge):
        if(len(self.nodes)>edge.node1.node_name and len(self.nodes[edge.node1.node_name])>edge.node2.node_name 
            and self.nodes[edge.node1.node_name][edge.node2.node_name]>0):
            self.nodes[edge.node1.node_name][edge.node2.node_name]=0
            return True
        return False
    
    def remove_node(self, node):
        if(len(self.nodes)>node.node_name):
            
            return True
        self.nodes.append([])
        for i in range(len(self.nodes)):
            self.nodes[i].append(0)
        return True

    def adjacent(self, node1, node2):
        pass
    
    def neighbors( self, node ):
        pass

a = construct_graph_from_file(AdjacencyMatrix(), "./Downloads/Python/cs4660-fall-2017-ammarbarafwala/cs4660/test/fixtures/graph-1.txt")

print(a.add_node(Node(0)))