from .map import Map

from numpy import rad2deg

class ClientMap(Map):

    def __init__(self):
        super().__init__()
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
        self.plt = plt
        self.Rectangle = Rectangle

    def print(self):
        self.plt.figure()
        for node in self.nodes:
            self.plt.scatter(*self.nodes[node], c='#0000FF')
            for neighbor in self.adjacency_list[node]:
                # print(self.nodes[node][0])
                self.plt.plot([self.nodes[node][0], self.nodes[neighbor][0]],[self.nodes[node][1], self.nodes[neighbor][1]], c='#FF0000')
        self.plt.show()

    def print_with_robot(self, position):
        x = position[0]
        y = position[1]
        theta = position[2]
        if self.plt.get_fignums():
            self.plt.clf()
        else:
            self.plt.figure()
            self.plt.ion()
            self.plt.show(block=False)

        for node in self.nodes:
            self.plt.scatter(*self.nodes[node], c='#0000FF')
            for neighbor in self.adjacency_list[node]:
                # print(self.nodes[node][0])
                self.plt.plot([self.nodes[node][0], self.nodes[neighbor][0]], [self.nodes[node][1], self.nodes[neighbor][1]],
                         c='#FF0000')

        width = 0.1 * 100
        height = 0.3 * 100
        self.plt.gca().add_patch(self.Rectangle((x-width/2, y-height/2), width, height,
                                      angle=rad2deg(theta),
                                      edgecolor='green',
                                      facecolor='green',
                                      lw=4,
                                      rotation_point='center'))
        self.plt.pause(0.05)
