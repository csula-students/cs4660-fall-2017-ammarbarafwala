"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""
import json
import time
from collections import deque
import heapq
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

def route_list(initial_id, current_id, G, G_name):
    route_list = []
    while current_id != initial_id:
        parent_id = G[current_id]
        route_list.append(G_name[parent_id] + '(' + parent_id + '):' 
        	+ G_name[current_id] + '(' + current_id + '):'
            + str(transition_state(parent_id, current_id)['event']['effect']))
        current_id = parent_id
    route_list.reverse()
    return  route_list


def bfs(initial_id, dest_id):
    G = {}
    G_name={}
    queue = deque()
    not_found = True
    queue.appendleft(initial_id)
    while queue and not_found:
        parent_id=queue.pop()
        room_state = get_state(parent_id)
        G_name[parent_id]=room_state['location']['name']
        for each_node in room_state['neighbors']:
            if each_node['id'] not in G:
                G[each_node['id']]=parent_id
                if dest_id==each_node['id']:
                    not_found = False
                    break
                queue.appendleft(each_node['id'])
    room_state = get_state(dest_id)
    G_name[dest_id] = room_state['location']['name']
    return route_list(initial_id,dest_id,G,G_name)

def dijkstra(initial_id, dest_id):
    queue = []
    G = {}
    S={}
    # heapq.heapify(queue)
    # heapq.heappush(queue, Data('',initial_id, None, 0))
    queue.append(Data('',initial_id, None, 0))
    while queue:
        print(len(queue))
        sorted(queue, key=lambda x: x.cost)
        parent_node = queue.pop()#heapq.heappop(queue)
        G[parent_node.id] = parent_node
        room_state = get_state(parent_node.id)
        parent_node.name=room_state['location']['name']
        for each_node in room_state['neighbors']:
            path_cost = parent_node.cost + transition_state(parent_node.id, each_node['id'])['event']['effect']
            if each_node['id'] not in G and (each_node['id'] not in S or S[each_node['id']].cost<path_cost):
                if each_node['id'] in S:
                    queue.remove(S[each_node['id']])
                data=Data('',each_node['id'], parent_node.id, path_cost)
                queue.append(data)
                S[each_node['id']]=data
                # heapq.heappush(queue, data)

    route_list = []
    print("hi")
    current_id = dest_id
    current_node = G[dest_id]
    while current_id != initial_id:
        parent_node=G[current_id]
        route_list.append(parent_node.name+'('+parent_node.id+'):'
                          +current_node.name+'('+current_node.id+'):'
                          +str(current_node.cost-parent_node.cost))
        current_id = parent_node.parent_id
        current_node=parent_node
    route_list.reverse()
    return route_list


class Data:
    def __init__(self, name, id, parent_id, cost):
        self.name = name
        self.id = id
        self.cost = cost
        self.parent_id = parent_id

    def __eq__(self, other):
        return self.cost == other.cost

    def __lt__(self, other):
        return self.cost < other.cost

if __name__ == "__main__":

    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    next_room = get_state("44dfaae131fa9d0a541c3eb790b57b00")
    path=dijkstra('7f3dc077574c013d98b2de8f735058b4','f1f131f647621a4be7c71292e79613f9')
    # print(empty_room)
    # print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
    for each_value in path:
        print(each_value)