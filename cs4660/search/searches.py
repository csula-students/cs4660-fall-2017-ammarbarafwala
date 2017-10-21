"""
Searches module defines all different search algorithms
"""
import heapq
from collections import deque

def bfs(graph, initial_node, dest_node):
    G = {}
    queue = deque()
    not_found = True
    queue.appendleft(initial_node)
    while queue and not_found:
        parent_node=queue.pop()
        for each_node in graph.neighbors(parent_node):
            if each_node not in G:
                G[each_node]=parent_node
                if dest_node==each_node:
                    not_found = False
                    break
                queue.appendleft(each_node)
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
    queue = []
    G = {}
    S={}
    heapq.heappush(queue, NodeDetail(initial_node,None,0))
    current_obj=None
    while queue:
        current_obj=heapq.heappop(queue)
        G[current_obj.node] = current_obj
        if current_obj.node == dest_node:
            break
        for child_node in graph.neighbors(current_obj.node):
            path_cost=current_obj.cost + graph.distance(current_obj.node, child_node)
            if child_node not in G:
                if child_node not in S:
                    data = NodeDetail(child_node, current_obj, path_cost)
                    S[child_node] = data
                    heapq.heappush(queue, data)
                elif S[child_node].cost > path_cost:
                    S[child_node].parent_obj = current_obj
                    S[child_node].cost = path_cost
    return route_list(graph, current_obj)

def route_list(graph ,current_obj):
    if current_obj.parent_obj is None:
        return []
    r_list=route_list(graph, current_obj.parent_obj)
    r_list.append(graph.get_edge(current_obj.parent_obj.node, current_obj.node))
    return r_list

class NodeDetail:

    def __init__(self, node, parent_obj, cost):
        self.node = node
        self.cost = cost
        self.parent_obj = parent_obj

    def __eq__(self, other):
        return self.cost == other.cost

    def __lt__(self, other):
        return self.cost < other.cost


def a_star_search(graph, initial_node, dest_node):
    queue = []
    G = {}
    S = {}
    heapq.heappush(queue, NodeDetail(initial_node, None, 0))
    current_obj = None
    while queue:
        current_obj = heapq.heappop(queue)
        G[current_obj.node] = current_obj
        if current_obj.node == dest_node:
            break
        for child_node in graph.neighbors(current_obj.node):
            path_cost = current_obj.cost + graph.distance(current_obj.node, child_node)
            if child_node not in G:
                if child_node not in S:
                    data = NodeDetail(child_node, current_obj, path_cost + heuristic(child_node, dest_node))
                    S[child_node] = data
                    heapq.heappush(queue, data)
                elif S[child_node].cost > path_cost:
                    S[child_node].parent_obj = current_obj
                    S[child_node].cost = path_cost + heuristic(child_node, dest_node)
    return route_list(graph, current_obj)

def heuristic(node, goal):
    dx = abs(node.data.x - goal.data.x)
    dy = abs(node.data.y - goal.data.y)
    # D is a scale value for you to adjust performance vs accuracy
    return 1 * (dx + dy)
