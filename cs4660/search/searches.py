"""
Searches module defines all different search algorithms
"""

from queue import Queue
from graph import graph

def bfs(grap, initial_node, dest_node):
    G = {}
    queue = Queue ()
    not_found = True
    queue.put(initial_node)
    while queue.not_empty and not_found:
        parent_node=queue.get()
        for each_node in grap.neighbors(parent_node):
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
        route_list.append(grap.get_edge(parent_node,current_node))
        current_node=parent_node
    route_list.reverse()
    return route_list

def dfs(grap, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass

def dijkstra_search(grap, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass

def a_star_search(grap, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass

def construct_graph(graph_path):
    """Helper function to construct graph given graph_path"""
    return lambda g: graph.construct_graph_from_file(g, graph_path)

# graph_1_path = 'c:/Users/ammar/Downloads/Python/cs4660-fall-2017-ammarbarafwala/cs4660/test/fixtures/graph-1.txt'
# graph_2_path = 'c:/Users/ammar/Downloads/Python/cs4660-fall-2017-ammarbarafwala/cs4660/test/fixtures/graph-2.txt'
# graph_1s = [graph.AdjacencyList(), graph.AdjacencyMatrix(), graph.ObjectOriented()]
# graph_2s = [graph.AdjacencyList(), graph.AdjacencyMatrix(), graph.ObjectOriented()]
# graph_1s = list(map(construct_graph(graph_1_path), graph_1s))
# graph_2s = list(map(construct_graph(graph_2_path), graph_2s))

# for g in graph_1s:
#     print(bfs(g, graph.Node(1), graph.Node(8))==[
#                     graph.Edge(graph.Node(1), graph.Node(3), 1),
#                     graph.Edge(graph.Node(3), graph.Node(10), 1),
#                     graph.Edge(graph.Node(10), graph.Node(8), 1)
#                 ],)
#     break