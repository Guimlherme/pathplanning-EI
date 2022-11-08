from .perception import Perception
from .map import Map

from math import sin, cos

TIMESTEP = 60e-3 #60ms

class State:
    def __init__(self, world_map : Map):
        self.theta = 0
        self.x = 0
        self.y = 0
        self.world_map = world_map
        self.node = 0

    def update(self, perception : Perception) -> None:
        self.theta += perception.angular_speed * TIMESTEP 
        self.x += perception.linear_speed * cos(self.theta) * TIMESTEP 
        self.y += perception.linear_speed * sin(self.theta) * TIMESTEP 

        self.node = self.world_map.get_closest_node(self.node, self.x, self.y)
    
    def found_target(self) -> bool:
        return True
    
    def object_detected(self) -> bool:
        return False