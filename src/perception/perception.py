import threading

class Perception:
    def __init__(self, angle, linear_speed, angular_speed, obstacle_distance):
        self.lock = threading.Lock()

        self.line_angle = angle
        self.linear_speed = linear_speed
        self.angular_speed = angular_speed
        self.obstacle_distance = obstacle_distance

    def set_line_angle(self, line_angle):
        with self.lock:
            self.line_angle = line_angle

    def set_linear_speed(self, linear_speed):
        with self.lock:
            self.linear_speed = linear_speed

    def set_angular_speed(self, angular_speed):
        with self.lock:
            self.angular_speed = angular_speed

    def set_obstacle_distance(self, obstacle_distance):
        with self.lock:
            self.obstacle_distance = obstacle_distance