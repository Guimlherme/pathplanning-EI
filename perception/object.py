import time
from constants import OBJECT_EXPIRATION_TIME


class Object:

    def __init__(self, initial_node, obstacle_node, world_map):
        self.world_map = world_map
        self.initial_node = initial_node
        self.obstacle_node = obstacle_node
        self.world_map.remove_edge(initial_node, obstacle_node)

        self.initial_time = time.time()

    def check_expiration(self):
        elapsed_time = time.time() - self.initial_time
        if elapsed_time > OBJECT_EXPIRATION_TIME:
            self.world_map.add_edge(self.initial_node, self.obstacle_node)
            return True
        return False
