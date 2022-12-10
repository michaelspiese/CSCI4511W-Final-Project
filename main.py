from queue import PriorityQueue
import matplotlib.pyplot as plt
import timeit

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

    def xy(self,start,end):
        return abs(start[0]-end[0]) + abs(start[1] - end[1])

    # The cost function for a*: f(n) = g(n) + h(n)
    def fn(self,gn,edge,weight,hn):
        return gn + weight*hn(edge,self.solution)


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

def create_path_dict(problem):
    pdict = {}
    for node in problem.nodes:
        pdict[node] = []
    return pdict

def make_map(map_paths,maps,colors,weights):
    fig = plt.figure(figsize=(7,11))
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    i = 0
    for map in maps:
        xy = ([],[])
        for pos in map:
            xy[0].append(pos[0])
            xy[1].append(pos[1])
        ax.scatter(xy[0],xy[1],c=colors[i],marker='o')
        i+=1
    ax.legend(weights,loc='upper right',title='Weights')
    for sPos in map_paths:
        for ePos in map_paths[sPos]:
            x = [sPos[0],ePos[0]]
            y = [sPos[1],ePos[1]]
            ax.plot(x,y,'black',linewidth=0.25,zorder=0)
    plt.title("A* Pathfinding with Varying Weights",fontsize='15')
    plt.show()

def weighted_astar_search(problem,start,hn,weight=1):
    i = 0
    frontier = PriorityQueue()
    frontier.put((problem.fn(0,start,weight,hn),0,start))
    problem.nodes[start].append(start)
    reached = {}
    paths = create_path_dict(problem)
    reached[start] = 0
    paths[start].append(start)
    while not frontier.empty():
        i += 1
        node = frontier.get()
        #print(node, i)
        if node[2] == problem.solution: return (node, i, paths[node[2]])
        for child in problem.nodes[node[2]]:
            path_cost = node[1]+problem.dist(node[2],child)
            if child not in reached or path_cost < reached[child]:
                reached[child] = path_cost
                frontier.put((problem.fn(path_cost,child,weight,hn),path_cost,child))
                paths[child] = paths[node[2]] + [child]
    return None

if __name__ == "__main__":
    mdict = create_map_dictionary("map.csv")
    g = Graph(mdict)
    start = (405,10005)
    #g.solution = (1384,5051)
    g.solution = (3045,5561)

    maps = []
    path_costs = []
    path_lengths = []
    iterations = []
    times = []
    #weights = [1,2,3,5,8]
    weights = [*range(0,11)]
    full_colors=['red','blue','green','yellow','pink','orange','brown','grey','purple','teal','gold']
    colors = []
    for weight in weights:
        ts = timeit.default_timer()
        search_data = weighted_astar_search(g,start,g.dist,weight)
        te = timeit.default_timer()
        maps.append(search_data[2])
        path_costs.append(search_data[0][1])
        path_lengths.append(len(search_data[2]))
        iterations.append(search_data[1])
        times.append((te-ts)*1000000)
        colors.append(full_colors[weight])
    print(str(path_lengths), str(path_costs), str(iterations), str(times))
    make_map(mdict,maps,colors,weights)
    