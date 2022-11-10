from .map import Map
from constants import DISTANCE_THRESHOLD, WHEEL_DIST
from .preprocessing_image import preprocessing_image

from math import sin, cos, pi

from threading import Lock
# An obstacle is considered as detected if it is closer than OBSTACLE_THRESHOLD for at least OBSTACLE_CYCLE_THRESHOLD cycles
OBSTACLE_THRESHOLD = 50
OBSTACLE_DETECTED_CYCLE_THRESHOLD = 10

class State:
    def __init__(self, world_map : Map, control_panel, system_clock, debug):
        self.lock = Lock()
        self.debug = debug

        self.theta = 0
        self.x = 0
        self.y = 0

        self.world_map = world_map
        self.node = 0
        
        self.obstacle_detected = False
        self.obstacle_detected_cycle_count = 0

        self.control_panel = control_panel

        self.system_clock = system_clock
        self.clock_id = system_clock.get_id()

        self.line_angle = 0
        self.linear_speed = 0
        self.angular_speed = 0
        self.obstacle_distance = 999

        self.right_encoder_previous = 0
        self.left_encoder_previous = 0
        self.previous_line_angle = 0

    def reset(self):
        self.x = self.control_panel.reset_values[0]
        self.y = self.control_panel.reset_values[1]
        self.theta = self.control_panel.reset_values[2]
        self.control_panel.reset_flag = False

    def update_from_sensors(self, right_encoder, left_encoder, obstacle_distance) -> None:
        if self.control_panel.reset_flag:
            self.reset()
        
        if self.debug:
            print("Previous Localization (x, y, theta) = ", self.x, self.y, self.theta)

        elapsed_time = self.system_clock.get_elapsed_time_since_last_call(self.clock_id)

        right_speed = (right_encoder - self.right_encoder_previous)/elapsed_time
        left_speed = (left_encoder - self.left_encoder_previous)/elapsed_time

        self.right_encoder_previous = right_encoder
        self.left_encoder_previous = left_encoder

        self.linear_speed = (right_speed + left_speed)/2
        self.angular_speed = (right_speed - left_speed)/WHEEL_DIST

        self.previous_theta = self.theta
        self.theta += self.angular_speed * elapsed_time 
        self.theta %= 2*pi

        self.x += self.linear_speed * cos(self.theta) * elapsed_time 
        self.y += self.linear_speed * sin(self.theta) * elapsed_time 
        
        self.node = self.world_map.get_closest_neighbor(self.node, self.x, self.y)

        with self.lock:
            self.previous_line_angle = self.line_angle
            self.line_angle += self.angular_speed * elapsed_time

        if obstacle_distance < OBSTACLE_THRESHOLD:
            if self.obstacle_detected_cycle_count < OBSTACLE_DETECTED_CYCLE_THRESHOLD:
                self.obstacle_detected_cycle_count += 1
            else:
                self.obstacle_detected = True
        else:
            self.obstacle_detected = False
        
        if self.debug:
            print("Encoders: ", right_encoder, left_encoder)
            print("Wheel Speeds: ", right_speed, left_speed)
            print("Linear and angular Speeds: ", self.linear_speed, self.angular_speed)
            print("Elapsed time since last localization update: %.3f ms" % (1000*elapsed_time)) 
            print("Localization (x, y, theta) = ", self.x, self.y, self.theta)
            print("Object distance: ", obstacle_distance, " obstacle detected = ", self.obstacle_detected)

    def update_vision(self, image):
        with self.lock: 
            self.line_angle = preprocessing_image(image)
            self.previous_line_angle = self.line_angle

    def position_is(self, target) -> bool:
        return abs(self.x - target[0]) < DISTANCE_THRESHOLD and abs(self.y - target[1]) < DISTANCE_THRESHOLD
    
    def intersection_detected(self) -> bool:
        for node, node_position in self.world_map.nodes.items():
            if self.position_is(node_position):
                return True
        return False