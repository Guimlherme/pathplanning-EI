from .perception import Perception
from .map import Map
from constants import DISTANCE_THRESHOLD

from math import sin, cos, pi

# An obstacle is considered as detected if it is closer than OBSTACLE_THRESHOLD for at least OBSTACLE_CYCLE_THRESHOLD cycles
OBSTACLE_THRESHOLD = 50
OBSTACLE_DETECTED_CYCLE_THRESHOLD = 10

class State:
    def __init__(self, world_map : Map, control_panel, system_clock, debug):
        self.theta = 0
        self.x = 0
        self.y = 0
        self.world_map = world_map
        self.node = 0

        self.debug = debug
        
        self.obstacle_detected = False
        self.obstacle_detected_cycle_count = 0

        self.control_panel = control_panel

        self.system_clock = system_clock
        self.clock_id = system_clock.get_id()

    def update(self, perception : Perception) -> None:
        if self.control_panel.reset_flag:
            self.x = self.control_panel.reset_values[0]
            self.y = self.control_panel.reset_values[1]
            self.theta = self.control_panel.reset_values[2]
            self.control_panel.reset_flag = False

        if self.debug:
            print("Previous Localization (x, y, theta) = ", self.x, self.y, self.theta)

        elapsed_time = self.system_clock.get_elapsed_time_since_last_call(self.clock_id)
        self.theta += perception.angular_speed * elapsed_time 
        self.theta %= 2*pi
        self.x += perception.linear_speed * cos(self.theta) * elapsed_time 
        self.y += perception.linear_speed * sin(self.theta) * elapsed_time 
        
        self.node = self.world_map.get_closest_neighbor(self.node, self.x, self.y)

        if perception.obstacle_distance < OBSTACLE_THRESHOLD:
            if self.obstacle_detected_cycle_count < OBSTACLE_DETECTED_CYCLE_THRESHOLD:
                self.obstacle_detected_cycle_count += 1
            else:
                self.obstacle_detected = True
        else:
            self.obstacle_detected = False
        
        if self.debug:
            print("Elapsed time since last localization update: %.3f ms" % (1000*elapsed_time)) 
            print("Localization (x, y, theta) = ", self.x, self.y, self.theta)
            print("Object distance: ", perception.obstacle_distance, " obstacle detected = ", self.obstacle_detected)

    
    def position_is(self, target) -> bool:
        return abs(self.x - target[0]) < DISTANCE_THRESHOLD and abs(self.y - target[1]) < DISTANCE_THRESHOLD
    
    def intersection_detected(self) -> bool:
        for node, node_position in self.world_map.nodes.items():
            if self.position_is(node_position):
                return True
        return False
