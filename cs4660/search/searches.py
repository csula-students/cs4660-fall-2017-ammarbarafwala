"""
Searches module defines all different search algorithms
"""

from queue import Queue
from graph import graph

def bfs(graph, initial_node, dest_node):
    G = {}
    queue = Queue ()
    not_found = True
    queue.put(initial_node)
    while queue.not_empty and not_found:
        parent_node=queue.get()
        for each_node in graph.neighbors(parent_node):
            if each_node not in G:
                G[each_node]=parent_node
                if dest_node==each_node:
                    not_found = False
                    break
                queue.put(each_node)
    route_list=[]
    current_node=dest_node
    while current_node!=initial_node:
        parent_node=G[current_node]
        route_list.append(graph.get_edge(parent_node,current_node))
        current_node=parent_node
    route_list.reverse()
    return route_list

def dfs(graph, initial_node, dest_node):
    node_path = dfs_helper(graph,initial_node,dest_node, {},[])
    
    edge_path=[]
    if node_path: 
        node_1=node_path[0]
        for index in range(1,len(node_path)):
            node_2 = node_path[index]
            edge_path.append(graph.get_edge(node_1,node_2))
            node_1=node_2
    return edge_path

def dfs_helper(graph, current_node, dest_node, visited_nodes, node_path):
    if current_node==dest_node:
        node_path.append(current_node)
    else:    
        for each_node in graph.neighbors(current_node):
            if each_node not in visited_nodes:
                visited_nodes[each_node]=current_node
                node_path.append(current_node)
                node_path=dfs_helper(graph, each_node,dest_node,visited_nodes,node_path)
                if node_path[len(node_path)-1]==dest_node:
                    return node_path
                node_path.pop()
    return node_path

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    Q = {}
    visited_nodes = []
    grey_nodes = []
    parent = {}
    nodes_distance = {}
    Q[initial_node] = 0
    parent[initial_node] = None
    nodes_distance[initial_node] = 0
    last_node = dest_node
    visited_nodes.append(initial_node)
    while (bool(Q)):
        current_node = min(Q, key=Q.get)
        Q.pop(current_node)
        visited_nodes.append(current_node)
        for neighbor in graph.neighbors(current_node):
            if ((neighbor not in visited_nodes and neighbor not in grey_nodes) or (nodes_distance[neighbor]>nodes_distance[current_node] + graph.distance(current_node, neighbor))):
                Q[neighbor] = nodes_distance[current_node] + graph.distance(current_node, neighbor)
                nodes_distance[neighbor] = nodes_distance[current_node] + graph.distance(current_node, neighbor)
                parent[neighbor] = current_node
                grey_nodes.append(neighbor)
        if (dest_node in visited_nodes):
            break
    list = []
    while parent[last_node] is not None:
        list = [graph.get_edge(parent[last_node], last_node)] + list
        last_node = parent[last_node]
    #print(list)
    return list
    pass

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass

def construct_graph(graph_path):
    """Helper function to construct graph given graph_path"""
    return lambda g: graph.construct_graph_from_file(g, graph_path)

graph_1_path = 'c:/Users/ammar/Downloads/Python/cs4660-fall-2017-ammarbarafwala/cs4660/test/fixtures/graph-1.txt'
graph_2_path = 'c:/Users/ammar/Downloads/Python/cs4660-fall-2017-ammarbarafwala/cs4660/test/fixtures/graph-2.txt'
graph_1s = [graph.AdjacencyList(), graph.AdjacencyMatrix(), graph.ObjectOriented()]
graph_2s = [graph.AdjacencyList(), graph.AdjacencyMatrix(), graph.ObjectOriented()]
graph_1s = list(map(construct_graph(graph_1_path), graph_1s))
graph_2s = list(map(construct_graph(graph_2_path), graph_2s))

for g in graph_1s:
    print( [
                    graph.Edge(graph.Node(1), graph.Node(2), 1),
                    graph.Edge(graph.Node(2), graph.Node(4), 1),
                    graph.Edge(graph.Node(4), graph.Node(5), 1),
                    graph.Edge(graph.Node(5), graph.Node(0), 1),
                    graph.Edge(graph.Node(0), graph.Node(7), 1),
                    graph.Edge(graph.Node(7), graph.Node(8), 1)
                ] ==
                dfs(g, graph.Node(1), graph.Node(8)))
    break