from math import sqrt
import matplotlib.pyplot as plt

class Map:
    def __init__(self):
        self.nodes = {}
        self.adjacency_list = { }

    def add_node(self, i, x, y):
        self.nodes[i] = (x, y)

    def add_edge(self, node1, node2):
        self._add_directed_edge(node1, node2)
        self._add_directed_edge(node2, node1)

    def _add_directed_edge(self, node1, node2):
        if node1 not in self.adjacency_list:
            self.adjacency_list[node1] = [node2]
        else:
            self.adjacency_list[node1].append(node2)

    def get_closest_node(self, node, x, y):
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

    def print(self):
        plt.figure()
        for node in self.nodes:
            plt.scatter(*self.nodes[node], c='#0000FF')
            for neighbor in self.adjacency_list[node]:
                print(self.nodes[node][0])
                plt.plot([self.nodes[node][0], self.nodes[neighbor][0]],[self.nodes[node][1], self.nodes[neighbor][1]], c='#FF0000')
        plt.show()


