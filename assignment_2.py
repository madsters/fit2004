class IdiotError(Exception):
    """
    For my amusement
    """
    pass

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
        # +2 for super sink
        res_graph = [[0 for i in range(size + 2)] for j in range(size + 2)]
        rev_graph = [[0 for i in range(size + 2)] for j in range(size + 2)]

        # !! TODO create super sink for each target
        for target in self.targets:
            res_graph[target][size + 1] = float('inf')
            rev_graph[size + 1][target] = 0

        return res_graph, rev_graph

    def get_flow(self):
        # sum flows from the source
        flow = 0
        for i in range(len(self.res_graph[self.source])):
            flow += self.res_graph[self.source][i]
        return flow

    def add_edge(self, u, v, capacity):
        # residual edge from u to v, flow = capacity
        self.res_graph[u][v] = capacity
        # reverse edge from v to u, flow = 0
        self.rev_graph[v][u] = 0
    
    def augment_path(self, path, flow):
        # path is list of tuples of (u, v)
        # min_capacity is int
        for edge in path:
            u = edge[0]
            v = edge[1]
            flow_direction = edge[2]

            # forward edge
            if flow_direction == 0 and self.res_graph[u][v]:
                self.res_graph[u][v] -= flow
                self.rev_graph[v][u] += flow
            # reverse edge
            elif flow_direction == 1 and self.rev_graph[v][u]:
                self.rev_graph[v][u] -= flow
                self.res_graph[u][v] += flow
            else:
                raise IdiotError("think i have the concept of reverse edges wrong lol")
            
        print('Success augmenting path with flow ', flow)

    def find_path_bfs(self):
        visited = []
        parents = [[None] for i in range(len(self.res_graph))]
        queue = [self.source]

        def backtrack(parents):
            # returns path from origin to target and min flow cap
            # O(D)
            # !! good chance this sucks
            path = []
            vertex = len(parents) - 1

            min_flow = float('inf')

            while vertex != self.source:
                path.append((parents[vertex][0], vertex, parents[vertex][1]))
                if parents[vertex][1] == 0:
                    if self.res_graph[parents[vertex][0]][vertex] < min_flow:
                        min_flow = self.res_graph[parents[vertex][0]][vertex]
                elif parents[vertex][0][1] == 1:
                    if self.rev_graph[parents[vertex][0]][vertex] < min_flow:
                        min_flow = self.rev_graph[parents[vertex][0]][vertex]
                else:
                    raise IdiotError("hmmmmmmmmmmmm what is going on lmao")
                vertex = parents[vertex][0]

            path.reverse()
            return path, min_flow

        found_path = False

        # while queue is not empty
        while queue:
            vertex = queue.pop()

            if vertex not in visited:
                visited.append(vertex)

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
                            parents[i] = (vertex, 0)
                        # valid path option! "reverse edge"
                        elif self.rev_graph[vertex][i] > 0:
                            # queue i
                            queue.append(i)
                            # set parent for i
                            parents[i] = (vertex, 1)
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
        graph.add_edge(connection[0], connection[1], connection[2])

    # find path O(D)
    path, min_flow = graph.find_path_bfs()
    while path:
        graph.augment_path(path, min_flow)
        path, min_flow = graph.find_path_bfs()
    return graph.get_flow()

# main
if __name__ == "__main__":
    connections = [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]
    maxIn = [5000, 3000, 3000, 3000, 2000]
    maxOut = [5000, 3000, 3000, 2500, 1500]
    origin = 0
    targets = [4, 2]
    print(maxThroughput(connections, maxIn, maxOut, origin, targets))
