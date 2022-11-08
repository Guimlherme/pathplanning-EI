from .perception import Perception
from .map import Map

from math import sin, cos

TIMESTEP = 60e-3 #60ms

# An obstacle is considered as detected if it is closer than OBSTACLE_THRESHOLD for at least OBSTACLE_CYCLE_THRESHOLD cycles
OBSTACLE_THRESHOLD = 0.3
OBSTACLE_DETECTED_CYCLE_THRESHOLD = 10

class State:
    def __init__(self, world_map : Map, control_panel):
        self.theta = 0
        self.x = 0
        self.y = 0
        self.world_map = world_map
        self.node = 0
        
        self.obstacle_detected = False
        self.obstacle_detected_cycle_count = 0

        self.control_panel = control_panel

    def update(self, perception : Perception) -> None:
        if self.control_panel.reset_flag:
            self.x = self.control_panel.reset_values[0]
            self.y = self.control_panel.reset_values[1]
            self.theta = self.control_panel.reset_values[2]
            self.control_panel.reset_flag = False

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
    
    def position_is(self, target) -> bool:
        return self.x == target[0] and self.y == target[1]
    