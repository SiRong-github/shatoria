class node:
    def __init__(self, power, colour, coordinates, next_node=None):
        self.power = power
        self.colour = colour
        self.coordinates = coordinates
        self.next_node = next_node

#     def set_next_node(self, next_node):
#         self.next_node = next_node

#     def get_next_node(self):
#         return self.next_node

#     def get_power(self):
#         return self.power

#     def get_colour(self):
#         return self.colour

#     def get_coordinates(self):
#         return self.coordinates


# # * Queueing Function
# # -> inserting & traversing nodes
# # * TupleToNode Function
# # -> traverse thru dictionary then create node for each tuple

# # * Priority Queue (BFS)
# # -> priority: distance of nodes closer to blue node; where you put the nodes
