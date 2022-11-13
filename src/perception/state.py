from .map import Map
from constants import DISTANCE_THRESHOLD, WHEEL_DIST, OBSTACLE_THRESHOLD
from .preprocessing_image import preprocessing_image
from .astar import find_path

from math import sin, cos, pi, sqrt
import numpy as np

from threading import Lock

# An obstacle is considered as detected if it is closer than OBSTACLE_THRESHOLD for at least OBSTACLE_CYCLE_THRESHOLD cycles
OBSTACLE_DETECTED_CYCLE_THRESHOLD = 10


class State:
    def __init__(self, world_map: Map, control_panel, system_clock, debug):
        self.lock = Lock()
        self.debug = debug

        # Theta, x, y are constrained to the world map
        self.theta = 0
        self.x = 0
        self.y = 0

        self.world_map = world_map
        self.node = 0
        self.next_waypoint = None

        self.obstacle_detected = False
        self.obstacle_detected_cycle_count = 0

        self.control_panel = control_panel

        self.system_clock = system_clock
        self.localization_clock_id = system_clock.get_id()
        self.vision_clock_id = system_clock.get_id()

        self.line_angle = 0
        self.linear_speed = 0
        self.angular_speed = 0
        self.obstacle_distance = 999

        self.right_encoder_previous = 0
        self.left_encoder_previous = 0
        self.previous_line_angle = 0

        self.left_wheel_command = 0
        self.right_wheel_command = 0

        self.vision_elapsed_time = 0
        self.localization_elapsed_time = 0

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

        elapsed_time = self.system_clock.get_elapsed_time_since_last_call(self.localization_clock_id)

        right_speed = np.sign(self.right_wheel_command) * (right_encoder - self.right_encoder_previous) / elapsed_time
        left_speed = np.sign(self.left_wheel_command) * (left_encoder - self.left_encoder_previous) / elapsed_time

        self.right_encoder_previous = right_encoder
        self.left_encoder_previous = left_encoder

        self.linear_speed = (right_speed + left_speed) / 2
        self.angular_speed = (right_speed - left_speed) / WHEEL_DIST

        # Updating map state
        self.previous_theta = self.theta
        if False:
            next_waypoint_pos = self.world_map.nodes[self.next_waypoint]
            cos_angulardelta = np.dot(self.y - next_waypoint_pos[1], self.x - next_waypoint_pos[0]) / \
                               (np.linalg.norm([self.x, self.y]) * np.linalg.norm(next_waypoint_pos))
            if cos_angulardelta > sqrt(3)/2:
                theta_est = self.theta + self.angular_speed * elapsed_time
                theta_est %= 2 * pi
                x_est = self.x + self.linear_speed * cos(self.theta) * elapsed_time
                y_est = self.y + self.linear_speed * sin(self.theta) * elapsed_time
                [self.x, self.y, self.theta] = self.world_map.find_position_on_grid(x_est, y_est, theta_est,
                                                                                    self.node, self.next_waypoint)
            else:
                self.theta += self.angular_speed * elapsed_time
                self.theta %= 2 * pi
                self.x += self.linear_speed * cos(self.theta) * elapsed_time
                self.y += self.linear_speed * sin(self.theta) * elapsed_time
        else:
            self.theta += self.angular_speed * elapsed_time
            self.theta %= 2 * pi
            self.x += self.linear_speed * cos(self.theta) * elapsed_time
            self.y += self.linear_speed * sin(self.theta) * elapsed_time


        self.node = self.identify_node()

        with self.lock:
            self.previous_line_angle = self.line_angle
            self.line_angle -= self.angular_speed * elapsed_time  # Camera referential is the opposite from world

        self.obstacle_distance = obstacle_distance
        self.localization_elapsed_time = elapsed_time

        if obstacle_distance < OBSTACLE_THRESHOLD:
            if self.obstacle_detected_cycle_count < OBSTACLE_DETECTED_CYCLE_THRESHOLD:
                self.obstacle_detected_cycle_count += 1
            else:
                self.obstacle_detected = True
        else:
            self.obstacle_detected = False

        if self.obstacle_detected:
            obstacle_x = self.x + obstacle_distance * cos(self.theta)
            obstacle_y = self.y + obstacle_distance * sin(self.theta)
            # print("REMOVING EDGE", self.node, self.obstacle_node)
            obstacle_node = self.world_map.get_closest_node(obstacle_x, obstacle_y)
            if self.world_map.has_edge(self.node, obstacle_node):
                self.world_map.remove_edge(self.node, obstacle_node)

        

        if self.debug:
            print("Encoders: ", right_encoder, left_encoder)
            print("Wheel Speeds: ", right_speed, left_speed)
            print("Linear and angular Speeds: ", self.linear_speed, self.angular_speed)
            print("Elapsed time since last localization update: %.3f ms" % (1000 * elapsed_time))
            print("Localization (x, y, theta) = ", self.x, self.y, self.theta)
            print("Object distance: ", obstacle_distance, " obstacle detected = ", self.obstacle_detected)
            print("Line angle: ", self.line_angle)

    def update_vision(self, image):
        elapsed_time = self.system_clock.get_elapsed_time_since_last_call(self.vision_clock_id)
        self.vision_elapsed_time = elapsed_time
        with self.lock:
            self.line_angle = preprocessing_image(image)
            self.previous_line_angle = self.line_angle

    def position_is(self, target) -> bool:
        return sqrt((self.x - target[0]) ** 2 + (self.y - target[1]) ** 2) < DISTANCE_THRESHOLD

    def intersection_detected(self) -> bool:
        for node, node_position in self.world_map.nodes.items():
            PARALEL_THRESHOLD = 5
            PERPENDICULAR_THRESHOLD = 20
            if (abs(self.x - node_position[0]) < PARALEL_THRESHOLD and abs(self.y - node_position[1]) < PERPENDICULAR_THRESHOLD) \
                or (abs(self.x - node_position[0]) < PERPENDICULAR_THRESHOLD and abs(self.y - node_position[1]) < PARALEL_THRESHOLD):
                print("Intersection detected", node_position)
                return True
        return False

    def identify_node(self):
        for node in self.world_map.adjacency_list[self.node]:
            node_position = self.world_map.nodes[node]
            if self.position_is(node_position):
                return node
        return self.node

    def update_next_waypoint(self, target_node):
        self.next_waypoint = self.plan(target_node)

    def plan(self, target_node):
        self.world_map.print()
        print("Searching from ", self.node, target_node)
        path = find_path(self.world_map, self.node, target_node)
        if path is None:
            print("PATH NOT FOUND")
            return self.node
        path_list = list(path)
        print("Path: ", path_list)
        if len(path_list) == 0:
            return self.node
        if len(path_list) == 1:
            return path_list[0]
        next_waypoint = path_list[1]
        return next_waypoint
