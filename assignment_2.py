def maxThroughput(connections, maxIn, maxOut, origin, targets):
    # create_graphs is O(D^2 + C), however D^2 + C < C^2 (every data centre has at least one connection), so O(C^2) dominates
    vertices, maxIn, maxOut, res_graph, rev_graph = create_graphs(connections, maxIn, maxOut, targets)
    max_flow = 0
    # super sinkkkkk
    target = len(res_graph) - 1
    min_cap, path = bfs(res_graph, maxIn, maxOut, origin, target)
    # while there is a path from origin to target in residual graph
    while path:
        max_flow += min_cap
        min_cap, path = bfs(res_graph, origin, targets)
    pass

def bfs(res_graph, rev_graph, maxIn, maxOut, origin, target):
    # returns list of tuples of path and graph traversed from origin to target (whichever one is found first)
    # and minimum capacity along path
    # graph traversed: 0 = res, 1 = rev
    # if no path found, returns none
    # graph is residual graph
    # maxIn and maxOut are lists of lists of [vertex, max in/out]
    # origin is vertex
    # targets is list of vertices
    # O(C^2)

    # initialise visited list
    visited = []
    parents = [[None] for i in range(len(res_graph))]
    # initialise path list
    path = []
    # initialise min capacity
    min_capacity = float('inf')
    queue = [origin]
    parent = None

    def backtrack(parents):
        # returns path from origin to target
        # O(D)
        # !! good chance this sucks
        path = []
        vertex = len(parents) - 1
        while vertex != origin:
            path.append((parents[vertex], vertex))
            vertex = parents[vertex]
        return path


    # while queue is not empty
    while next_vertex:
        vertex = queue.pop()

        if vertex not in visited:
            visited.append(vertex)
            parents.append(parent)

            # end of path!
            if vertex == target:
                return min_capacity, path
            
            
            # for each neighbour of vertex
            for i in range(len(res_graph[vertex])):
                if i not in visited:
                    # valid path option! "forward edge"
                    if res_graph[vertex][i] > 0 and maxIn:
                        next_vertex = i
                        path.append((vertex, next_vertex, 0))
                        # get min flow
                        if res_graph[vertex][i] < min_capacity:
                            min_capacity = res_graph[vertex][i]
                        break
                    # valid path option! "reverse edge"
                    elif rev_graph[vertex][i] > 0:
                        next_vertex = i
                        path.append((vertex, next_vertex, 0))
                        # get min flow
                        if rev_graph[vertex][i] < min_capacity:
                            min_capacity = rev_graph[vertex][i]
                        break
                    else:
                        # edge full/no edge!
                        continue
            
    return min_capacity, backtrack(parents)


def create_graphs(connections, max_in, max_out, targets):
    """
    Function description: Creates a graph as a list of vertices and an adjacency list from the given connections, as 
    well as a residual graph
    Graphs include super sink
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
    # create empty matrix with three nodes per data centre O(D^2), + 2*3 for super sink
    res_graph = [[0 for i in range(3*(max + 2))] for j in range(3*(max + 2))]
    rev_graph = [[0 for i in range(3*(max + 2))] for j in range(3*(max + 2))]
    # create adjacency matrix O(C)
    i = 0
    for connection in connections:
        # residual edge from u to v, flow = capacity
        res_graph[connection[0]][connection[1]] = connection[2]
        # reverse edge from v to u, flow = 0
        rev_graph[connection[1]][connection[0]] = 0
    # create edges from super sink to targets O(D)
    for target in targets:
        res_graph[-1][target] = float('inf')
        rev_graph[target][-1] = float('inf')
        res_graph[-2][target] = float('inf')
        rev_graph[target][-2] = float('inf')
        res_graph[-3][target] = float('inf')
        rev_graph[target][-3] = float('inf')

    return vertices, max_in_new, max_out_new, res_graph, rev_graph
    
