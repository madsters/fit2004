"""
CapacityFlowGraph class, has single source and super sink
"""
class CapacityFlowGraph:
    def __init__(self, size, source, targets):
        self.source = source
        self.size = size
        self.targets = targets
        self.res_graph, self.rev_graph = self.__create_graphs(self.size)
    
    def __create_graphs(self, size):
        # +2 for super sink, *3 for in, out
        res_graph = [[0 for i in range(3*(size + 2))] for j in range(3*(size + 2))]
        rev_graph = [[0 for i in range(3*(size + 2))] for j in range(3*(size + 2))]

        # create super sink
        for target in self.targets:
            res_graph[-1][target] = float('inf')
            rev_graph[target][-1] = float('inf') 
            res_graph[-2][target] = float('inf')
            rev_graph[target][-2] = float('inf')
            res_graph[-3][target] = float('inf')
            rev_graph[target][-3] = float('inf')

        return res_graph, rev_graph

    def add_edge(self, u, v, capacity, uout, vin):
        u_index = self.vertex_to_index(u)
        v_index = self.vertex_to_index(v)

        # residual edge from u to v, flow = capacity
        self.res_graph[u_index][v_index] = capacity
        # reverse edge from v to u, flow = 0
        self.rev_graph[v_index][u_index] = 0

        # residual edge from u to uout, flow = uout, residual edge from vin to v, flow = vin
        self.res_graph[u_index][u_index + 1] = uout
        self.res_graph[v_index - 1][v_index] = vin
        # reverse edge from uout to u, flow = 0, reverse edge from v to vin, flow = 0
        self.rev_graph[u_index + 1][u_index] = 0
        self.rev_graph[v_index][v_index - 1] = 0

    def vertex_to_index(vertex):
        return vertex*3 + 1
    
    def index_to_vertex(index):
        return index//3
    
    def augment_path(self, path, flow):
        # path is list of tuples of (u, v)
        # min_capacity is int
        for edge in path:
            u = edge[0]
            v = edge[1]
            flow = edge[2]

            # forward edge
            if self.res_graph[u][v] >= flow:
                self.res_graph[u][v] -= flow
                self.rev_graph[v][u] += flow
            # reverse edge
            elif self.rev_graph[v][u] >= flow:
                self.rev_graph[v][u] -= flow
                self.res_graph[u][v] += flow
            else:
                raise ValueError("Invalid path")
            
        print('Success augmenting path with flow ', flow)

    def find_path_bfs(self):
        visited = []
        parents = [[None] for i in range(len(self.res_graph))]
        # initialise path list
        path = []
        # initialise min capacity
        min_capacity = float('inf')
        queue = [self.vertex_to_index(self.source)]
        parent = None

        def backtrack(parents):
            # returns path from origin to target and min flow cap
            # O(D)
            # !! good chance this sucks
            path = []
            vertex = len(parents) - 1

            min_flow = float('inf')

            while vertex != self.vertex_to_index(self.source):
                path.append((parents[vertex], vertex))
                if self.res_graph[parents[vertex]][vertex] < min_flow:
                vertex = parents[vertex]

            return path.reverse()

        found_path = False

        # while queue is not empty
        while queue:
            vertex = queue.pop()

            if vertex not in visited:
                visited.append(vertex)
                parents[vertex] = parent

                # end of path!
                if vertex == len(self.res_graph) - 1:
                    found_path = True
                    break
                
                # for each neighbour of vertex
                for i in range(len(self.res_graph[vertex])):
                    if i not in visited:
                        # valid path option! "forward edge"
                        if self.res_graph[vertex][i] > 0:
                            # queue i
                            queue.append(i)
                            # set parent for i
                            parents[i] = vertex
                        # valid path option! "reverse edge"
                        elif self.rev_graph[vertex][i] > 0:
                            # queue i
                            queue.append(i)
                            # set parent for i
                            parents[i] = vertex
                        # edge full/no edge!
                        else:
                            continue
                

        if not found_path:
            return None, None
        
        return backtrack(parents)


    


def maxThroughput(connections, maxIn, maxOut, origin, targets):
    max = 0
    # find no. data centres O(C)
    for connection in connections:
        if connection[0] > max:
            max = connection[0]
        if connection[1] > max:
            max = connection[1]
    
    graph = CapacityFlowGraph(max, origin, targets)

    # create adjacency matrix O(C)
    for connection in connections:
        graph.add_edge(connection[0], connection[1], connection[2], maxIn[connection[0]], maxOut[connection[1]])

