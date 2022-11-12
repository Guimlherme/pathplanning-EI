from math import sqrt

#import matplotlib.pyplot as plt
#from matplotlib.patches import Rectangle

class Map:
    def __init__(self):
        self.nodes = {}
        self.adjacency_list = { }

    def add_node(self, i, x, y):
        self.nodes[i] = (x, y)

    def add_edge(self, node1, node2):
        self._add_directed_edge(node1, node2)
        self._add_directed_edge(node2, node1)

    def remove_edge(self, node1, node2):
        self.adjacency_list[node1].remove(node2)
        self.adjacency_list[node2].remove(node1)

    def _add_directed_edge(self, node1, node2):
        if node1 not in self.adjacency_list:
            self.adjacency_list[node1] = [node2]
        else:
            self.adjacency_list[node1].append(node2)

    def get_closest_neighbor(self, node, x, y):
        node_position = self.nodes[node]
        min_dist = sqrt( (node_position[0] - x)**2 + (node_position[1] - y)**2)
        min_dist_node = node

        for neighbor in self.adjacency_list[node]:
            neighbor_position = self.nodes[neighbor]
            dist = sqrt( (neighbor_position[0] - x)**2 + (neighbor_position[1] - y)**2)
            if dist < min_dist:
                min_dist = dist
                min_dist_node = neighbor

        return min_dist_node


    def get_closest_node(self, x, y):
        # -1 to know it is the first
        min_dist = -1
        min_dist_node = -1

        for neighbor, position in self.nodes.items():
            dist = sqrt( (position[0] - x)**2 + (position[1] - y)**2)
            if dist < min_dist or min_dist == -1:
                min_dist = dist
                min_dist_node = neighbor

        return min_dist_node





