"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""
from graph import graph
import json
from queue import Queue
import codecs



# http lib import for Python 2 and 3: alternative 4

try:

    from urllib.request import urlopen, Request

except ImportError:

    from urllib2 import urlopen, Request



GET_STATE_URL = "http://192.241.218.106:9000/getState"

STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"



def get_state(room_id):

    """

    get the room by its id and its neighbor

    """

    body = {'id': room_id}

    return __json_request(GET_STATE_URL, body)



def transition_state(room_id, next_room_id):

    """

    transition from one room to another to see event detail from one room to

    the other.



    You will be able to get the weight of edge between two rooms using this method

    """

    body = {'id': room_id, 'action': next_room_id}

    return __json_request(STATE_TRANSITION_URL, body)



def __json_request(target_url, body):

    """

    private helper method to send JSON request and parse response JSON

    """

    req = Request(target_url)

    req.add_header('Content-Type', 'application/json; charset=utf-8')

    jsondata = json.dumps(body)

    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

    req.add_header('Content-Length', len(jsondataasbytes))

    reader = codecs.getreader("utf-8")

    response = json.load(reader(urlopen(req, jsondataasbytes)))

    return response

def bfs(initial_id, dest_id):
    G = {}
    queue = Queue ()
    not_found = True   
    queue.put(initial_id)
    while queue.not_empty and not_found:
        parent_id=queue.get()
        room_state = get_state(parent_id)
        for each_node in room_state['neighbors']:
            if each_node['id'] not in G:
                G[each_node['id']]=parent_id
                if dest_id==each_node['id']:
                    not_found = False
                    break
                queue.put(each_node['id'])
    route_list=[]
    current_id=dest_id
    room_state=get_state(current_id)
    current_name=room_state['location']['name']+'('+current_id+")"
    while current_id!=initial_id:
        parent_id=G[current_id]
        room_state=get_state(parent_id)
        parent_name=room_state['location']['name']+'('+parent_id+")"
        route_list.append(parent_name+':'+current_name+":"+str(transition_state(parent_id,current_id )['event']['effect']))
        current_id=parent_id
        room_state=get_state(current_id)
        current_name=room_state['location']['name']+'('+current_id+")"
    route_list.reverse()
    return route_list

def dijkstra(initial_node, dest_node):
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
        room_state = get_state(current_node)
        for each_neighbor in room_state['neighbors']:
            neighbor=each_neighbor['id']
            distance=transition_state(current_node,neighbor )['event']['effect']
            if ((neighbor not in visited_nodes and neighbor not in grey_nodes) or (nodes_distance[neighbor]>nodes_distance[current_node] + distance)):
                Q[neighbor] = nodes_distance[current_node] + distance
                nodes_distance[neighbor] = nodes_distance[current_node] + distance
                parent[neighbor] = current_node
                grey_nodes.append(neighbor)
        if (dest_node in visited_nodes):
            break
    list = []
    while parent[last_node] is not None:
        list = [parent[last_node]+':'+last_node] + list
        last_node = parent[last_node]
    #print(list)
    return list
    pass

if __name__ == "__main__":

    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    next_room = get_state("44dfaae131fa9d0a541c3eb790b57b00")
    path=bfs('7f3dc077574c013d98b2de8f735058b4','f1f131f647621a4be7c71292e79613f9')
    #print(empty_room["location"])
    for each_value in path:
        print(each_value)