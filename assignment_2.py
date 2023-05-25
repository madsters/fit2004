def maxThroughput(connections, maxIn, maxOut, origin, targets):
    # create_graphs is O(D^2 + C), however D^2 + C < C^2 (every data centre has at least one connection), so O(C^2) dominates
    vertices, adjacencies = create_graphs(connections)
    pass

def bfs(graph, origin, target):
    pass    

def create_graphs(connections):
    """
    Function description: Creates a graph as a list of vertices and an adjacency list from the given connections, as 
    well as a residual graph
    :Input:
    connections: list of edges with max flow along the edge
    :Output, return or postcondition: vertices: list of vertices, graph: adjacency list
    :Time complexity: O(D^2 + C)
    :Aux space complexity: O(D^2 + C)
    """
    max = 0
    # find no. data centres O(C)
    for connection in connections:
        if connection[0] > max:
            max = connection[0]
        if connection[1] > max:
            max = connection[1]
    vertices = list(range(max + 1))
    # create empty matrix O(D^2)
    graph = [[0 for i in range(max + 1)] for j in range(max + 1)]
    res_graph = [[0 for i in range(max + 1)] for j in range(max + 1)]
    # create adjacency matrix O(C)
    for connection in connections:
        # residual edge from u to v, flow = capacity
        graph[connection[0]][connection[1]] = connection[2]
        # reverse edge from v to u, flow = 0
        res_graph[connection[1]][connection[0]] = 0
    return vertices, graph, res_graph
    
