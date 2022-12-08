
# Data type needs:
#    - Node Value (position tuple)
#    - Connected nodes (List of point tuples, dictionary of distances?)
class Graph:
    def __init__(self,nodes=None):
        if nodes is None:
            nodes = {}
        self.nodes = nodes
    def getVertices(self):
        return list(self.nodes.keys())

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
    g = Graph(create_map_dictionary("map.csv"))
    print(len(g.nodes))
    