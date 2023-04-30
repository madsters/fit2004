import assignment_1

"""
Test adjacency list
"""

locations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
roads = [(0, 3, 4, 5), (3, 4, 4, 5), (3, 8, 23, 0), (4, 3, 2, 0), (2, 5, 1, 4), (8, 9, 23, 0)]

ad_list = assignment_1.get_adjacency_list(roads, locations)
#print(ad_list)

# adjacency list working

"""
Test add passenger flags
"""
passengers = [4]
ad_list_passengers = assignment_1.add_passenger_flags(ad_list, passengers)
#print(ad_list_passengers)

# passenger flags working

"""
TEST Q1
"""

# Example
start = 0
end = 4
# The locations where there are potential passengers
passengers = [2, 1]
# The roads represented as a list of tuple
roads = [(0, 3, 5, 3), (3, 4, 35, 15), (3, 2, 2, 2), (4, 0, 15, 10),
(2, 4, 30, 25), (2, 0, 2, 2), (0, 1, 10, 10), (1, 4, 30, 20)]
# Your function should return the optimal route (which takes 27 minutes).
print(assignment_1.optimalRoute(start, end, passengers, roads))
[0, 3, 2, 0, 3, 4]

"""
Test shortest path
"""

shortest_path = assignment_1.dijkstra_shortest_path(ad_list_passengers, 0)
#print(shortest_path)

"""
Test select sections
"""
occupancy_probability = [
[31, 54, 94, 34, 12],
[26, 25, 24, 16, 87],
[39, 74, 50, 13, 82],
[42, 20, 81, 21, 52],
[30, 43, 19, 5, 47],
[37, 59, 70, 28, 15],
[ 2, 16, 14, 57, 49],
[22, 3, 9876, 19, 99]]

#print(assignment_1.select_sections(occupancy_probability))

# select sections working