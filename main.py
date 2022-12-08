from queue import PriorityQueue

class Graph:
    def __init__(self,nodes=None):
        if nodes is None:
            nodes = {}
        self.nodes = nodes
        self.solution = None

    def getVertices(self):
        return list(self.nodes.keys())

    def getEdges(self,node):
        return self.nodes[node]
    
    # Find distance from one point to another
    def dist(self,start,end):
        return ((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5

    # The cost function for a*: f(n) = g(n) + h(n)
    def fn(self,gn,edge,weight):
        return gn + weight*self.dist(edge,self.solution)


def create_map_dictionary(filename):
    mdict = {}
    minneapolis = open(filename, "r")
    lines = minneapolis.readlines()
    for line in lines:
        points = line.strip().split(",")
        start = (int(points[1]),int(points[2]))
        end = (int(points[3]),int(points[4]))
        if start not in mdict:
            mdict[start] = [end]
        else:
            mdict[start].append(end)

        # Since we're ignoring 1-way streets, make sure that streets running in the opposite direction are in the dictionary
        if end not in mdict:
            mdict[end] = [start]
        elif start not in mdict[end]:
            mdict[end].append(start)

    # Return the populated dictionary
    return mdict

def weighted_astar_search(problem,start,weight=1):
    frontier = PriorityQueue()
    frontier.put((problem.fn(0,start,weight),0,start))
    reached = {}
    reached[start] = 0
    while not frontier.empty():
        node = frontier.get()
        print(node)
        if node[2] == problem.solution: return node
        for child in problem.nodes[node[2]]:
            path_cost = node[1]+problem.dist(node[2],child)
            if child not in reached or path_cost < reached[child]:
                reached[child] = path_cost
                frontier.put((problem.fn(path_cost,child,weight),path_cost,child))
    return None

if __name__ == "__main__":
    g = Graph(create_map_dictionary("map.csv"))
    print(g.nodes[(465,9964)])
    start = (405,10005)
    g.solution = (1384,5051)
    node = weighted_astar_search(g,start)
    