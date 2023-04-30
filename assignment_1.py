"""
QUESTION 1
"""
import heapq

def optimalRoute(start, end, passengers, roads):
    """
    Function description:
    optimalRoute takes a start and end location, a list of passengers and a list of roads and returns the shortest path
    between the start and end location that considers the any improvement in time that can be made by carrying
    passengers.

    Approach description:
    The approach taken is to first create an adjacency list of the roads, then add a boolean flag to each location
    in the adjacency list to represent whether or not there is a passenger at that location. The adjacency list is then
    passed to a modified Dijkstra's algorithm that takes into account the passenger flag.

    :Input:
        start: integer representing the start location
        end: integer representing the end location
        passengers: list of integers representing the locations of passengers
        roads: list of directed graph edge tuples (a, b, c, d), called a 'road' (R) where
            a and b are the start and end points of the edge, respectively
            c and d are weightings of the edge in certain cases (referred as accompanied/unaccompanied)
    :Output: list of integers representing the shortest path between the start and end location
    :Time complexity:
    :Aux space complexity:
    """
    # find maximum road location to determine size of adjacency list | T: O(R)
    max = 0
    for road in roads:
        if road[0] > max:
            max = road[0]
    locations = range(max)

    # create adjacency list | T: O(L), S: O(L + R)
    adjacency_list = get_adjacency_list(roads, locations)
    # add passenger flags to adjacency list | T: O(P + L), S: O(1)
    adjacency_list = add_passenger_flags(adjacency_list, passengers)
    # find shortest path | 
    shortest_path = dijkstra_shortest_path(adjacency_list, start, end)

    return shortest_path

def get_adjacency_list(roads: tuple, locations: list) -> list:
    """
    Function description:
    get_adjacency_list creates an adjacency list for the tuples in roads

    :Input:
        roads: list of directed graph edge tuples (a, b, c, d), called a 'road' (R) where 
            a and b are the start and end points of the edge, respectively
            c and d are weightings of the edge in certain cases (referred as accompanied/unaccompanied)
    :Output: adjecency list that also stores weighting at each data point
    :Time complexity: O(L + log(L)) ~ O(L)
    :Aux space complexity: O(L + R)
    """
    # create empty adjacency list, S: O(L)
    size = len(locations)
    adjacency_list = [[] for loc in range(size)]
    # for each road, add the data to the adjacency list | T: O(R), S: O(L + R)
    for road in roads:
        location = road[0]
        destination = road[1]
        weightings = (road[2], road[3])
        adjacency_list[location].append((destination, weightings))
    # return the list
    return adjacency_list

def add_passenger_flags(adjacency_list: list, passengers) -> list:
    """
    Function description:
    takes an adjacency list of location lists, appending an additional boolean to each location list representing
    whether or not there is a passenger at that particular location.

    :Input:
        adjacency_list: list of lists of tuples representing the destination that can be reached from a certain 
        location as well as the time taken to reach that destination accompanied/unaccompanied
    :Output: adjecency list of lists with boolean flags appended at each location
    :Time complexity: O(P) + O(L)
        note O(P) < O(L) as P can be at most size |L|
    :Aux space complexity: O(1)
    """
    # add false flags to all locations
    for location in adjacency_list:
        location.append(False)
    # add true flags to locations specified in passengers list | T: O(P)
    for location in passengers:
        if not adjacency_list[location][-1]:
            adjacency_list[location][-1] = True
    return adjacency_list

def dijkstra_shortest_path(adjacency_list: list, start: int) -> list:
    """
    Function description:
    Uses a modified Dijkstra's algorithm to find the shortest path. The modification utilises recursion to redefine
    start and endpoints once the path encounters a passenger. When a passenger can be added to the car, the function is called 
    again with the accompanied flag set to true, and finds the shortest path based on there being passengers in the car.

    :Input:
        adjacency_list: list of lists of tuples representing the destination that can be reached from a certain
        location as well as the time taken to reach that destination accompanied/unaccompanied
        start: integer representing the start location
        accompanied: boolean representing whether or not there is a passenger in the car
    :Output: list of integers representing the shortest path between the start and end location
    :Time complexity: O(R log(L) + L log(L)) ~ O(R log(L)); the R term dominates in the worst case as R can be 
        at most L^2.
    :Aux space complexity: O(L)
    """
    # initialise distances, predecessors and queue 
    predecessors = [None for i in range(len(adjacency_list))]
    distances = []

    # set all distances to infinity and accompanied flag to 0 (False)
    # distances will keep track of the shortest time to reach a location, as well as if that shortest time
    # included an accompanying passenger.
    # it can be assumed that once a passenger is picked up, they will travel with the car until the end of the journey
    for i in range(len(adjacency_list)):
        distances.append((float('inf'), 0))
    queue = []
    
    # set start distance to 0 and check for passengers at start location
    # push start distance and node to queue
    if adjacency_list[start][-1]:
        accompanied = 1
    else: 
        accompanied = 0
    distances[start] = (0, accompanied)
    heapq.heappush(queue, (0, start))
    
    while queue: 
        # pop node with smallest distance from queue
        # pops start node initially
        # will pop node with smallest distance from start node in next iteration
        # note that smallest distances takes into account whether or not the previous node had
        # a passenger in the car
        current_distance, current_node = heapq.heappop(queue)

        # check if current node has a passenger
        if distances[current_node][1] or adjacency_list[current_node][-1]:
            accompanied = 1

        # for each neighbour of current node, relax the distance if shorter than current distance
        # distance will depend on whether or not the current node has a passenger
        for neighbour in adjacency_list[current_node]: 
            # passenger flag, not a nieghbour!
            if type(neighbour) == bool:
                continue
            neighbour_node = neighbour[0]
            neighbour_distance = neighbour[1][accompanied]
            relax(distances, queue, predecessors, current_node, neighbour_node, neighbour_distance, accompanied)
            
    return distances, predecessors

def relax(distances: list, distances_heap: list, predecessors: list, u: int, v: int, dist_u_to_v: int, accompanied: int) -> None:
    """
    Function description:
    relaxes the distance of a node v from a node u if the distance from u to v is less than the current distance of v,
    or if the distance from u to v is equal to the current distance of v and u has a passenger in the car.
    pushes the new distance and node to the queue.
    if the distance can be relaxed, and u's accompanied flag == 1, then v's flag is set to 1 if not already.
    if the distance can be relaxed, and u's accompanied flag == 0, then v's flag is set to 0 if not already.

    :Input:
        distances: list of distances from a node to the start node
        u: node to relax distance from
        v: node to relax distance to
    :Output: None
    :Time complexity: O(log(L)) worst case
    :Aux space complexity: O(1)
    """
    if distances[u][0] + dist_u_to_v < distances[v][0] or (distances[u][0] + dist_u_to_v == distances[v][0] and accompanied == 1):
        distances[v] = (distances[u][0] + dist_u_to_v, accompanied)
        heapq.heappush(distances_heap, (dist_u_to_v + distances[u][0], v)) # O(log(L))
        predecessors[v] = u

"""
QUESTION 2
"""

def select_sections(occupancy_probability):
    """
    Function description:

    Approach description:
    My approach uses dynamic programming to break down the problem. We're essentially finding a path of least resistance
    through the occupancy probability matrix, where the resistance is the occupancy probability of a section. 
    To break this down, we need to find the path of least resistance to each cell. 
    We can do this by finding the path of least resistance to each adjacent (diagonally or vertically) cell in the row 
    above, and then adding the resistance of the current cell to the path of least resistance to the cell above it.
    Building up a matrix of running distance in this way, the minimum value in the final row of the matrix will be the
    end of the path of least resistance through the occupancy probability matrix. 
    Then we backtrack through the matrix, always choosing the path based on minimum adjacent value of the running total 
    in that row. 
    This approach solves the problem in small sections, and then uses the solutions to find the larger solution.
    
    An auxillary function get_min(row) is used to convenietly return the index and value of the minimum in a row.
    """
    running_total = [[0 for row in occupancy_probability] for col in occupancy_probability[0]]
    running_total[0] = occupancy_probability[0]
    # build matrix of running totals
    for i, row in enumerate(occupancy_probability):
        if i == 0:
            continue
        for j, col in enumerate(row):
            options = [occupancy_probability[i-1][j-1], occupancy_probability[i-1][j], occupancy_probability[i-1][j+1]]
            running_total[i][j] = col + min(options)
    # find minimum value in final row
    min_index, min_value = get_min(running_total[-1])
    # backtrack through matrix
    path = []
    for i in range(len(running_total) - 1, -1, -1):
        # add index to path
        path.append((i, min_index))
        # find minimum value in adjacent cells in the row above
        min_index, min_value = get_min(running_total[i-1][min_index-1], running_total[i-1][min_index], running_total[i-1][min_index+1])
    return path

def get_min(row):
    """
    Function description:
    returns the index and value of the minimum in a row

    :Input:
        row: list of values
    :Output:
        index: index of minimum value
        value: minimum value
    :Time complexity: O(n)
    :Aux space complexity: O(1)
    """
    min_index = 0
    min_value = row[0]
    for i, value in enumerate(row):
        if value < min_value:
            min_index = i
            min_value = value
    return min_index, min_value
            
"""
Helper classes
"""

class distance_priority_queue():
    """
    Priority queue implementation.

    """
    def __init__(self, list):
        self.queue = list 
        self.min = self.__get_min() # O(n)
    
    def queue(self, node, distance):
        self.queue.append((node, distance))
        if distance < self.min[1]:
            self.min = (node, distance)
    
    def pop(self):
        if len(self.queue) == 0:
            return None 
        self.queue.remove(self.min) # O(n)
        self.min = min(self.queue) # O(n)
        return self.min
    
    def __get_min(self):
        current_min = (None, float('inf'))
        for item in self.queue:
            if item[1] < self.min[1]:
                current_min = item
        return current_min
    