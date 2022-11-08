from .perception import Perception
from .map import Map

from math import sin, cos

TIMESTEP = 60e-3 #60ms

# An obstacle is considered as detected if it is closer than OBSTACLE_THRESHOLD for at least OBSTACLE_CYCLE_THRESHOLD cycles
OBSTACLE_THRESHOLD = 0.3
OBSTACLE_DETECTED_CYCLE_THRESHOLD = 10

class State:
    def __init__(self, world_map : Map):
        self.theta = 0
        self.x = 0
        self.y = 0
        self.world_map = world_map
        self.node = 0
        
        self.obstacle_detected = False
        self.obstacle_detected_cycle_count = 0

    def update(self, perception : Perception) -> None:
        self.theta += perception.angular_speed * TIMESTEP 
        self.x += perception.linear_speed * cos(self.theta) * TIMESTEP 
        self.y += perception.linear_speed * sin(self.theta) * TIMESTEP 

        self.node = self.world_map.get_closest_node(self.node, self.x, self.y)

        if perception.obstacle_distance < OBSTACLE_THRESHOLD:
            if self.obstacle_detected_cycle_count < OBSTACLE_DETECTED_CYCLE_THRESHOLD:
                self.obstacle_detected_cycle_count += 1
            else:
                self.obstacle_detected = True
        else:
            self.obstacle_detected = False
    
    def found_target(self) -> bool:
        return True
    