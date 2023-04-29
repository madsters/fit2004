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
    # create empty adjacency list | T: O(L), S: O(L)
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
    # add false flags to all locations | T: O(L)
    for location in adjacency_list:
        location.append(False)
    # add true flags to locations specified in passengers list | T: O(P)
    for location in passengers:
        if not adjacency_list[location][-1]:
            adjacency_list[location][-1] = True
    return adjacency_list

def dijkstra_shortest_path(adjacency_list: list, start: int, end: int, accompanied=False) -> list:
    """
    Function description:
    Uses a modified Dijkstra's algorithm to find the shortest path. The modification utilises recursion to redefine
    start and endpoints once the path encounters a passenger. When a passenger can be added to the car, the function is called 
    again with the accompanied flag set to true, and finds the shortest path based on there being passengers in the car.

    """
    
    pass


