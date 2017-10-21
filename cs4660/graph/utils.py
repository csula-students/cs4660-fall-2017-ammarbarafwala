from . import graph

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x) + str(self.y) + self.symbol)

def parse_grid_file(g, file_path):
    x=0
    y=0
    f = open(file_path)
    data = f.read()
    data = data.split('\n')
    i =0
    while i < len(data):
        j=0
        while j <len(data[i]):
            if (data[i][j] == '-' or data[i][j] =='+'):
                x -=1
                break
            elif (data[i][j] == '|'):
                j +=1
                continue
            elif (data[i][j] == '#' and data[i][j+1] =='#'):
                 j +=2
                 y +=1
                 continue
            else:
                a = graph.Node(Tile(y,x,data[i][j]+data[i][j+1]))
                g.add_node(a)
                y +=1
                j +=2
        y =0
        x +=1
        i +=1
    x = 0
    y = 0
    f = open(file_path)
    data = f.read()
    data = data.split('\n')
    i = 0
    while i < len(data):
        j = 0
        while j < len(data[i]):
            if (data[i][j] == '-' or data[i][j] == '+'):
                x -= 1
                break
            elif (data[i][j] == '|'):
                j += 1
                continue
            elif (data[i][j] == '#' and data[i][j + 1] == '#'):
                j += 2
                y += 1
                continue
            else:
                if (data[i + 1][j] != '-' and data[i + 1][j] != '+' and data[i + 1][j] != '#' and data[i + 1][
                    j] != '|'):
                    a = graph.Node(Tile(y, x, data[i][j] + data[i][j + 1]))
                    b = graph.Node(Tile(y, x + 1, data[i + 1][j] + data[i + 1][j + 1]))
                    g.add_edge(graph.Edge(a, b, 1))
                if(data[i][j+2] != '-' and data[i][j+2] != '+' and data[i][j+2] != '#' and data[i][j+2] !='|'):
                    a = graph.Node(Tile(y,x,data[i][j]+data[i][j+1]))
                    b = graph.Node(Tile(y+1,x,data[i][j+2]+data[i][j+3]))
                    g.add_edge(graph.Edge(a, b, 1))
                if (data[i][j - 1] != '-' and data[i][j - 1] != '+' and data[i][j - 1] != '#' and data[i][
                        j - 1] != '|'):
                    a = graph.Node(Tile(y, x, data[i][j] + data[i][j + 1]))
                    b = graph.Node(Tile(y - 1, x, data[i][j -2] + data[i][j -1]))
                    g.add_edge(graph.Edge(a, b, 1))
                if (data[i - 1][j] != '-' and data[i - 1][j] != '+' and data[i - 1][j] != '#' and data[i - 1][
                    j] != '|'):
                    a = graph.Node(Tile(y, x, data[i][j] + data[i][j + 1]))
                    b = graph.Node(Tile(y, x - 1, data[i - 1][j] + data[i - 1][j + 1]))
                    g.add_edge(graph.Edge(a, b, 1))
                y += 1
                j += 2
        y = 0
        x += 1
        i += 1
    return g

def convert_edge_to_grid_actions(edges):
    a = ""
    for edge in edges:
        from_node = edge.from_node
        to_node = edge.to_node
        from_tile_x = from_node.data.x
        from_tile_y = from_node.data.y
        to_tile_x = to_node.data.x
        to_tile_y = to_node.data.y

        if(from_tile_x -to_tile_x >0):
            a += "W"
        elif (from_tile_x - to_tile_x < 0):
            a +="E"
        elif (from_tile_y - to_tile_y > 0):
            a += "N"
        elif (from_tile_y - to_tile_y < 0):
            a += "S"
    return a
