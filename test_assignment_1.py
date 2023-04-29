import assignment_1

"""
Test adjacency list
"""

locations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
roads = [(0, 3, 4, 5), (4, 1, 2, 10), (2, 5, 1, 4)]

ad_list = assignment_1.get_adjacency_list(roads, locations)
print(ad_list)

# adjacency list working

"""
Test add passenger flags
"""
passengers = [0, 1, 9]
ad_list_passengers = assignment_1.add_passenger_flags(ad_list, passengers)
print(ad_list_passengers)

# passenger flags working
