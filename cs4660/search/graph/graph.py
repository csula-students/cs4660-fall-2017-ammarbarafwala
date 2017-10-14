"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
"""

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object

    note that grpah object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:

    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """
    f = open(file_path, encoding='utf-8')
    first_line = f.readline()
    for i in range(int(first_line)):
        graph.add_node(Node(i))
    text = f.read()
    lines = text.split('\n')
    for line in lines:
        if len(line) > 0:
            values = line.split(':')
            edge = Edge( Node( int( values[0] ) ), Node( int( values[1] ) ), int( values[2] ) )
            graph.add_edge(edge)
    return graph

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        if(node_1 in self.adjacency_list):
            for each_edge in self.adjacency_list[node_1]:
                if(each_edge.to_node == node_2):
                    return True
        return False

    def neighbors(self, node):
        node_neighbors=[]
        if(node in self.adjacency_list):
            for each_edge in self.adjacency_list[node]:
                node_neighbors.append(each_edge.to_node)
            return node_neighbors
        return []

    def add_node(self, node):
        if(node in self.adjacency_list):
            return False
        self.adjacency_list[node]=[]
        return True

    def remove_node(self, node):
        if(node not in self.adjacency_list):
            return False
        del self.adjacency_list[node]
        for each_key in self.adjacency_list:
            for each_edge in self.adjacency_list[each_key]:
                if(each_edge.to_node == node):
                    self.adjacency_list[each_key].remove(each_edge)
                    break
        return True

    def add_edge(self, edge):
        self.add_node(edge.from_node)
        if(edge in self.adjacency_list[edge.from_node]):
            return False
        self.adjacency_list[edge.from_node].append(edge)
        return True

    def remove_edge(self, edge):
        if(edge.from_node in self.adjacency_list and edge in self.adjacency_list[edge.from_node]):
            self.adjacency_list[edge.from_node].remove(edge)
            return True
        return False

    def get_edge(self,node_1,node_2):
        for each_edge in self.adjacency_list[node_1]:
            if each_edge.to_node == node_2:
                return each_edge
        return None

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        return self.adjacency_matrix[self.__get_node_index(node_1)][self.__get_node_index(node_2)] > 0

    def neighbors(self, node):
        connected_nodes = self.adjacency_matrix[self.__get_node_index(node)]
        node_neighbors = []
        for i in range(len(connected_nodes)):
            if connected_nodes[i] > 0:
                node_neighbors.append(self.nodes[i])
        return node_neighbors

    def add_node(self, node):
        if node in self.nodes:
            return False
        self.nodes.append(node)
        for i in range(len(self.adjacency_matrix)):
            self.adjacency_matrix[i].append(0)
        new_row = []
        for j in range(len(self.adjacency_matrix) + 1):
            new_row.append(0)
        self.adjacency_matrix.append(new_row)
        return True

    def remove_node(self, node):
        if node not in self.nodes:
            return False
        index = self.__get_node_index(node)
        for each_list in self.adjacency_matrix:
            each_list.pop(index)
        self.adjacency_matrix.remove(self.adjacency_matrix[index])
        self.nodes.remove(node)
        return True

    def add_edge(self, edge):
        from_node_index = self.__get_node_index(edge.from_node)
        to_node_index = self.__get_node_index(edge.to_node)
        if edge.to_node not in self.nodes or edge.from_node not in self.nodes or self.adjacency_matrix[from_node_index][to_node_index] > 0:
            return False
        self.adjacency_matrix[from_node_index][to_node_index] = edge.weight
        return True

    def remove_edge(self, edge):
        from_node_index = self.__get_node_index(edge.from_node)
        to_node_index = self.__get_node_index(edge.to_node)
        if self.adjacency_matrix[from_node_index][to_node_index] > 0:
            self.adjacency_matrix[from_node_index][to_node_index] = 0
            return True
        return False

    def __get_node_index(self, node):
        """helper method to find node index"""
        return self.nodes.index(node)

    def get_edge(self,node_1,node_2):
        return self.adjacency_matrix[self.__get_node_index(node_1)][self.__get_node_index(node_2)]

class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        neighbors = self.neighbors(node_1)
        return node_2 in neighbors

    def neighbors(self, node):
        neighbors = []
        for each_edge in self.edges:
            if (each_edge.from_node == node):
                neighbors.append(each_edge.to_node)
        return neighbors

    def add_node(self, node):
        if node in self.nodes:
            return False
        self.nodes.append(node)
        return True

    def remove_node(self, node):
        for each_edge in self.edges:
            if each_edge.from_node == node or each_edge.to_node == node:
                self.edges.remove(each_edge)
        if node in self.nodes:
            self.nodes.remove(node)
            return True
        return False

    def add_edge(self, edge):
        if edge in self.edges or edge.from_node not in self.nodes or edge.to_node not in self.nodes:
            return False
        self.edges.append(edge)
        return True

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        return False

    def get_edge(self,node_1,node_2):
        for each_edge in self.edges:
            if each_edge.from_node == node_1 and each_edge.to_node == node_2:
                return each_edge
        return None