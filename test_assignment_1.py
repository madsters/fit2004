import assignment_1

"""
Test adjacency list
"""

locations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
roads = [(0, 3, 4, 5), (3, 4, 4, 5), (3, 8, 23, 0), (4, 3, 2, 0), (2, 5, 1, 4), (8, 9, 23, 0)]

ad_list = assignment_1.get_adjacency_list(roads, locations)
print(ad_list)

# adjacency list working

"""
Test add passenger flags
"""
passengers = [4]
ad_list_passengers = assignment_1.add_passenger_flags(ad_list, passengers)
print(ad_list_passengers)

# passenger flags working

"""
Test shortest path
"""



shortest_path = assignment_1.dijkstra_shortest_path(ad_list_passengers, 0)
print(shortest_path)