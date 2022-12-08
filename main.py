from queue import PriorityQueue

class Graph:
    def __init__(self,solution,nodes=None):
        if nodes is None:
            nodes = {}
        self.nodes = nodes
        self.solution = solution

    def getVertices(self):
        return list(self.nodes.keys())

    def getEdges(self,node):
        return self.nodes[node]
    
    # Find heuristic value from node to solution
    def hn(self,start,end):
        return ((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5

    # Find minimum heuristic value from node's edges to solution
    def minhn(self,node):
        low = [(100000,100000),100000]
        edges = self.getEdges(node)
        for edge in edges:
            dist = self.hn(edge,self.solution)
            print(edge,dist)
            if dist < low[1]:
                low = [edge,dist]
        return low


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
    return mdict

if __name__ == "__main__":
    g = Graph((810,10256),create_map_dictionary("map.csv"))
    n = (1384,5051)
    minimum = g.minhn(n)
    print(minimum)

    