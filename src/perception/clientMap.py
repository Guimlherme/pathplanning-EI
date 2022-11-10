import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from .map import Map

class ClientMap(Map):

    def print(self):
        plt.figure()
        for node in self.nodes:
            plt.scatter(*self.nodes[node], c='#0000FF')
            for neighbor in self.adjacency_list[node]:
                # print(self.nodes[node][0])
                plt.plot([self.nodes[node][0], self.nodes[neighbor][0]],[self.nodes[node][1], self.nodes[neighbor][1]], c='#FF0000')
        plt.show()

    def print_with_robot(self, state):
        plt.figure()
        for node in self.nodes:
            plt.scatter(*self.nodes[node], c='#0000FF')
            for neighbor in self.adjacency_list[node]:
                # print(self.nodes[node][0])
                plt.plot([self.nodes[node][0], self.nodes[neighbor][0]], [self.nodes[node][1], self.nodes[neighbor][1]],
                         c='#FF0000')
        width = 0.1
        height = 0.3
        plt.gca().add_patch(Rectangle((state.x-width/2, state.y-height/2), width, height,
                                      angle=rad2deg(state.theta),
                                      edgecolor='green',
                                      facecolor='green',
                                      lw=4,
                                      rotation_point='center'))
        plt.show()