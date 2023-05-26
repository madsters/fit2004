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
        """
        Function description: initializes the capacity flow graph, creates residual and reverse graphs
        Input: 
            size: int number of nodes in the graph
            source: int index of source node
            targets: list of int indices of target nodes
        Output: creates CapacityFlowGraph object
        Time complexity: O(D^2)
        Auxiliary space complexity: O(D^2)
        """
        self.source = source
        self.size = size + 1
        self.targets = targets
        self.res_graph, self.rev_graph = self.__create_graphs()
    
    def __create_graphs(self):
        """
        Function description: initlializes the residual and reverse graphs
        Input: NA
        Output: residual graph, reverse graph
        Time complexity: O(D^2) < O(C^2)
        Auxiliary space complexity: O(D^2)
        """
        # *3 for maxin/maxout, +1 for super sink
        res_graph = [[0 for i in range(3*(self.size) + 1)] for j in range(3*(self.size) + 1)]
        rev_graph = [[0 for i in range(3*(self.size) + 1)] for j in range(3*(self.size) + 1)]

        self.graph_size = len(res_graph)

        # create super sink connected to each target
        for target in self.targets:
            res_graph[target][self.graph_size - 1] = float('inf')
            rev_graph[self.graph_size - 1][target] = float('inf')
            self.super_sink = self.graph_size - 1

        return res_graph, rev_graph

    def get_node_in(self, node):
        """
        Function description: gets the equivalent in node of a node
        Input: NA
        Output: node index int
        Time complexity: O(1)
        Auxiliary space complexity: O(0)
        """
        return node + self.size
    
    def get_node_out(self, node):
        """
        Function description: gets the equivalent out node of a node
        Input: NA
        Output: node index int
        Time complexity: O(1)
        Auxiliary space complexity: O(0)
        """
        return node + 2*(self.size)

    def get_flow(self):
        """
        Function description: gets the flow from the reversible flow graph (used when network is saturated)
        Input: NA
        Output: flow int
        Time complexity: O(D^2) < O(C^2)
        Auxiliary space complexity: O(0)
        """
        # sum flows into the self.targets from the reversible flow graph
        flow = 0
        for target in self.targets:
            for i in range(len(self.rev_graph[target])):
                flow += self.rev_graph[target][i]
        return flow

    def add_edge(self, u, v, capacity):
        """
        Function description: adds edge from u to v with capacity
        Input:
            u: index of node u
            v: index of node v
        Output: none, modifies self.res_graph and self.rev_graph
        Time complexity: O(1)
        Auxiliary space complexity: O(0)
        """
        # residual edge from u to v, flow = capacity
        self.res_graph[u][v] = capacity
        # reverse edge from v to u, flow = 0
        self.rev_graph[v][u] = 0
    
    def augment_path(self, path, flow):
        """
        Function description: augments the path with flow
        Input:
            path: list of tuples of (u, v, flow_direction)
            flow: int value of flow value to augment
        Output: none, modifies self.res_graph and self.rev_graph, updates flow
        Time complexity: O(path) = O(D) worst case
        Auxiliary space complexity: O(0)
        """
        # path is list of tuples of (u, v)
        # min_capacity is int
        for edge in path:
            u = edge[0]
            v = edge[1]
            flow_direction = edge[2]

            # no need to augment if super sink
            if v == self.super_sink or u == self.super_sink:
                continue

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
            

    def find_path_bfs(self):
        """
        Function description: finds a path from source to super sink using bfs
        Input: None
        Output: path from source to super sink, min flow capacity
        Time complexity: O(D) < O(C) 
        Auxiliary space complexity: O(D)
        """
        visited = []
        parents = [[None] for i in range(len(self.res_graph))]
        queue = [self.source]

        def backtrack(parents):
            """
            Function description: backtracks from super sink to source to find path + min flow capacity
            Input:
                parents: list of tuples of (parent, flow_direction)
            Output: path from source to super sink, min flow capacity
            Time complexity: O(D) < O(C) 
            Auxiliary space complexity: O(D)
            """
            path = []
            vertex = len(parents) - 1

            min_flow = float('inf')

            while vertex != self.source:
                path.append((parents[vertex][0], vertex, parents[vertex][1]))
                if parents[vertex][1] == 0:
                    if self.res_graph[parents[vertex][0]][vertex] < min_flow:
                        min_flow = self.res_graph[parents[vertex][0]][vertex]
                elif parents[vertex][0][1] == 1:
                    if self.rev_graph[vertex][parents[vertex][0]] < min_flow:
                        min_flow = self.rev_graph[vertex][parents[vertex][0]]
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
    """
    Function description: takes in a list of connections, max in/out for each data centre, origin and targets and returns the max throughput
    of the network
    Approach: create a graph with 3n + 1 nodes, where n is the number of data centres. The first n nodes represent the data centres, the next n
    nodes represent the data centres' in edge, and the last n nodes represent the data centres' out edge. The last node is the super sink.
    The edges are added as follows in the residual graph:
    - connections are from data centre out node to data centre in node, with capacity = connection capacity
    - maxin to node, capacity = maxin
    - node to maxout, capacity = maxout
    - target to super sink, capacity = inf
    In the reverse graph, capacities start at 0 representing the reversible flow (apart from super sink, infinite)
    CapacityFlowGraph manages the residual and reverse graphs, and has methods to find a path and augment the path with flow
    The main loop finds a path, augments the path with the min flow, and repeats until no path is found
    Inputs:
    connections: list of tuples of (data centre 1, data centre 2, capacity)
    maxIn: list of max in for each data centre
    maxOut: list of max out for each data centre
    origin: origin data centre
    targets: list of target data centres
    Time complexity: looking at inline comments, O(C + C + D + D + C + C*D*C) ~ O(C^2*D) worst case as required
    Based on the assumption that D < C, so D is approximately C in the worst case
    """
    max = 0
    # find no. data centres O(C)
    for connection in connections:
        if connection[0] > max:
            max = connection[0]
        if connection[1] > max:
            max = connection[1]
    
    graph = CapacityFlowGraph(max, origin, targets)

    # create adjacency matrix for edge flows O(C)
    for connection in connections:
        graph.add_edge(graph.get_node_out(connection[0]), graph.get_node_in(connection[1]), connection[2])
    
    # create adjacency matrix for max in/out O(D) < O(C) (every data centre has at least 1 connection)
    for i in range(len(maxIn)):
        graph.add_edge(graph.get_node_in(i), i, maxIn[i])
        graph.add_edge(i, graph.get_node_out(i), maxOut[i])

    path, min_flow = graph.find_path_bfs() # O(C)
    while path: # O(C*D*C)
        graph.augment_path(path, min_flow) # O(D)
        path, min_flow = graph.find_path_bfs() # O(C)
    return graph.get_flow()


class TrieNode:
    CAT_DICTIONARY_SIZE = 26
    def __init__(self, char: str):
        """
        Function description: create a trienode with a character and a list of children nodes (initially empty), 
        and a counter to indicate how many times the node completes a sentence
        :Input:
        char: character of the node
        :Output, return or postcondition: TrieNode object
        :Time complexity: O(1) - cat dictionary is constant size
        :Aux space complexity: O(1) - cat dictionary is constant size
        """
        # normal node
        if char:        
            self.char = char
        # root node
        else: 
            self.char = "None"
        
        # tracking how many times node completes a sentence
        self.end_of_word = 0

        self.children = [None for i in range(self.CAT_DICTIONARY_SIZE)]


    def add_child(self, child):
        """
        Function description: add a child to the TrieNode object based on the character index of the child
        :Input:
        child: a TrieNode
        :Output, return or postcondition: the index of the character in the children list points to the child TrieNode
        :Time complexity: O(1)
        :Aux space complexity: O(0)
        """
        self.children[child.get_char_index()] = child

    def ends_sentence(self):
        """
        Function description: add an end of word counter to node
        :Input: NA
        :Output, return or postcondition: the current node end of word counter is incremented by 1
        :Time complexity: O(1)
        :Aux space complexity: O(0)
        """
        self.end_of_word += 1
    
    def get_child(self, char: str):
        """
        Function description: get a child to the node by character
        :Input:
        char: a character
        :Output, return or postcondition: TrieNode or None representing the child
        :Time complexity: O(1)
        :Aux space complexity: O(0)
        """
        return self.children[ord(char) - ord('a')]
    
    def get_char_index(self):
        """
        Function description: get the index of the character in the cat dictionary to map to the children list
        :Input: NA
        :Output, return or postcondition: int representing the index of the character in the cat dictionary
        :Time complexity: O(1)
        :Aux space complexity: O(0)
        """
        return ord(self.char) - ord('a')
    
    def __str__(self):
        """
        Function description: returns a string representation of the node, used for visualisation
        :Input: NA
        :Output: string representation of the node
        :Time complexity: O(1)
        :Aux space complexity: O(0)
        """
        return self.char
    
    def visualise(self):
        """
        Function description: visualise the Trie
        :Input: NA
        :Output: NA
        :Not doing complexity this is just for me:
        """
        self.visualise_aux(self, 0)
    
    def visualise_aux(self, node, level):
        """
        Function description: visualise the trie
        :Input: 
        node: a trie node
        level: int representing the level of the node in the trie
        :Output: NA
        :Not doing complexity this is just for me:
        """
        if node:
            print(' ' * level, node)
            for child in node.children:
                self.visualise_aux(child, level + 1)



class CatsTrie:
    CAT_DICTIONARY_SIZE = 26
    def __init__(self, sentences: list):
        """
        Function description: create a CatsTrie with the sentences given
        CatsTrie is a Trie graph of the sentences given, with each node representing a word in the cat dictionary
        :Input:
        sentences: list of strings representing the sentences to be added to the trie
        :Output, return or postcondition: CatsTrie object
        :Time complexity: O(N*M) where N is the number of sentences and M is the length of the longest sentence
        :Aux space complexity: O(N*M)
        """
        self.sentences = sentences
        self.trie = TrieNode(None)
        self.build_trie() # O(N*M)
    
    def build_trie(self):
        for sentence in self.sentences: # O(N) where N is the number of sentences
            self.add_sentence(sentence) # O(M)

    def add_sentence(self, sentence: str):
        """
        Function description: add a sentence to the CatsTrie
        :Input:
        sentence: string representing the sentence to be added to the trie
        :Output, return or postcondition: sentence given is found in CatsTrie, or if already found, the end of word counter for
         the final node is incremented
        :Time complexity: O(M) where M is the length of the longest sentence
        :Aux space complexity: O(1)
        """
        node = self.trie
        for char in sentence: # worst case O(M) where M is the length of the longest sentence
            if not node.get_child(char):
                node.add_child(TrieNode(char))
            node = node.get_child(char)
        # keeping track of number of times a sentence is added
        node.ends_sentence()

    def autocomplete(self, prefix: str):
        """
        Function description: autocomplete a sentence given a prefix
        Approach description: my approach uses a BFS to traverse all the subtrees of the prefix. It keeps track of the current best
        completion and the number of occurences of the current best completion. It then compares the current best completion with
        the current node's completion and updates the current best completion if the current node's completion is better (i.e. has
        more occurences). If the current node's completion is the same as the current best completion, then the lexigraphically
        smaller one is chosen. 
        :Input:
        prefix: string representing the prefix of the sentence to be autocompleted 
        :Output, return or postcondition: string representing the best completion of the prefix
        :Time complexity: O(X + Y) where X is the length of the prefix and Y is the length of the most frequent completion of the prefix
        :Aux space complexity: O(X + Y) where X is the length of the prefix and Y is the length of the most frequent completion of the prefix
        """
        from collections import deque

        # get to the last node of the prefix - O(X) where X is the length of the prefix
        node = self.trie
        for char in prefix:
            index = ord(char) - ord('a')
            if node.children[index] is None:
                return None
            node = node.children[index]

        completion = ""
        queue = deque([(node, prefix)])

        # need to keep track of how many occurences the current best completion has
        occurences = 0

        # BFS to traverse all subtrees of the prefix
        while queue:
            node, word = queue.popleft()

            # Check if the node represents a complete sentence that is a better completion than the current sentence
            if node.end_of_word > occurences:
                completion = word
                occurences = node.end_of_word
            elif node.end_of_word == occurences and node.end_of_word != 0:
                if word < completion: # lexicographical size
                    completion = word

            # Add child nodes to the queue
            for i, child in enumerate(node.children): # O(26) = O(1)
                if child is not None:
                    char = chr(ord('a') + i)
                    queue.append((child, word + char))

        return completion

