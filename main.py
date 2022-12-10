from queue import PriorityQueue
import matplotlib.pyplot as plt
import timeit

############################## DATA STRUCTURES ###############################
# Data structure containing problem data: graph of potisions and cost function
class Graph:
    def __init__(self,nodes):
        self.nodes = nodes

    # The cost function for a*: f(n) = g(n) + h(n)
    def fn(self,gn,edge,solution,weight,hn):
        return gn + weight*hn(edge,solution)
    

################# HEURISTIC FUNCTIONS ################
# Find distance from one point to another (ADMISSIBLE)
def dist(start,end):
    return ((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5

# Find distance by traveling along x then y (INADMISSIBLE)
def xy(start,end):
    return abs(start[0]-end[0]) + abs(start[1] - end[1])

################################################## DATA ORGANIZATION FUNCTIONS #################################################
# Import the Minneapolis map data and transform it into a dictionary of nodes that map to a list of the nodes it is connected to
def create_map_dictionary(filename):
    # Open the minneapolis map and save all lines to a list
    minneapolis = open(filename, "r")
    lines = minneapolis.readlines()
    minneapolis.close()

    # Add data to a dictionary of points mapping to a list of connected points
    mdict = {}
    for line in lines:
        # Arrange line data into position tuples
        points = line.strip().split(",")
        start = (int(points[1]),int(points[2]))
        end = (int(points[3]),int(points[4]))

        # For each point, append the end node to the start node's connection list
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

# Create a dictionary entry for every node to save the path taken from the start node to the solution node
def create_path_dict(problem):
    pdict = {}
    for node in problem.nodes:
        pdict[node] = []
    return pdict

##################################################### OUTPUT GENERATION FUNCTIONS ####################################################
# From the data obtained by the search, visualize it in a scatterplot on top of the visual map of the Minneapolis graph data structure
def make_map(map_paths,maps,colors,weights,hn):
    # Create and format a figure
    fig = plt.figure(figsize=(7,11))
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    plt.title("Weighted A* Pathfinding with Varying Weight",fontsize='15')

    # Map all paths taken for each weight in different colors
    i=0
    for map in maps:
        xy = ([],[])
        for pos in map:
            xy[0].append(pos[0])
            xy[1].append(pos[1])
        ax.scatter(xy[0],xy[1],c=colors[i],marker='o')
        i+=1

    # Add the legend to the figure with only the search data
    ax.legend(weights,loc='upper right',title='Weights')

    # Create the roadmap of minneapolis underneath the search data
    for sPos in map_paths:
        for ePos in map_paths[sPos]:
            x = [sPos[0],ePos[0]]
            y = [sPos[1],ePos[1]]
            ax.plot(x,y,'black',linewidth=0.25,zorder=0)

    # Save the figure to a vector graphic and show the figure
    filename = hn.__name__ + "_{w:d}Weights.svg"
    plt.savefig(filename.format(w=len(weights)))
    plt.show()

# Save all execution data to a csv file
def createCSV(weights,costs,lengths,times,iterations,hn):
    filename = hn.__name__ + "_{w:d}Weights.csv"
    out = open(filename.format(w=len(weights)),'w')
    out.write("Weight,Cost,Length,Iterations,Time\n")
    for i in range(len(weights)):
        out.write(str(weights[i])+","+str(costs[i])+","+str(lengths[i])+","+str(iterations[i])+","+str(times[i])+"\n")
    out.close()

############################### SEARCH FUNCTIONS ###############################
# Performs Weighted A* Search on the problem structure with specified heuristic
def weighted_astar_search(problem,start,solution,hn,weight=1):
    # Variable used to keep track of nodes searched
    i = 0

    # Create a priority queue and place the starting node in it
    frontier = PriorityQueue()
    frontier.put((problem.fn(0,start,solution,weight,hn),0,start))

    # Create a dictionary to keep track of all nodes that have been searched already
    reached = {}
    reached[start] = 0

    # Create a dictionary to store paths taken to get to each node from the start node
    paths = create_path_dict(problem)
    paths[start].append(start)

    # Search through frontier for solution, add nodes to frontier if unreached or more efficient upon expansion
    while not frontier.empty():
        i += 1
        node = frontier.get()
        if node[2] == solution: return (node, i, paths[node[2]])
        for child in problem.nodes[node[2]]:
            path_cost = node[1]+dist(node[2],child)
            if child not in reached or path_cost < reached[child]:
                reached[child] = path_cost
                frontier.put((problem.fn(path_cost,child,solution,weight,hn),path_cost,child))
                paths[child] = paths[node[2]] + [child]
    
    # Return none if search fails
    return None

########################################################################### MAIN ###########################################################################
############################################################################################################################################################
if __name__ == "__main__":
    # Create the dictionary representation of the data and use it to make a graph
    mdict = create_map_dictionary("map.csv")
    g = Graph(mdict)

    # Define start node, solution node, weights to apply, heuristic function, and colors to plot
    start = (405,10005)
    #g.solution = (1384,5051)
    solution = (3045,5561)
    #weights = [0]
    weights = [1,2,3,5,8]
    #weights = [*range(11)]
    hn = dist
    full_colors=['red','blue','green','yellow','pink','orange','brown','grey','purple','teal','gold']

    # Lists to store search execution data
    maps = []
    path_costs = []
    path_lengths = []
    iterations = []
    times = []
    colors = []

    # Iterate through every weight specified
    for weight in weights:
        # Perform search and record execution time
        ts = timeit.default_timer()
        search_data = weighted_astar_search(g,start,solution,hn,weight)
        te = timeit.default_timer()

        # Save search execution data to corresponding lists
        maps.append(search_data[2])
        path_costs.append(search_data[0][1])
        path_lengths.append(len(search_data[2]))
        iterations.append(search_data[1])
        times.append((te-ts)*1000000)
        colors.append(full_colors[weight])

    # Save the output data in both a csv of execution data and an svg of the visialized map
    createCSV(weights,path_costs,path_lengths,times,iterations,hn)
    make_map(mdict,maps,colors,weights,hn)
    