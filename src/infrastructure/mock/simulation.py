from math import pi, sin, cos
from constants import DISTANCE_THRESHOLD, WHEEL_DIST

class Simulation:
    def __init__(self, system_clock) -> None:
        self.x = 0
        self.y = 0
        self.theta = 0
        self.system_clock = system_clock
        self.clock_id = system_clock.get_id()

        self.right_speed = 0 
        self.left_speed = 0
        self.distance = 0

        self.right_encoder_value = 0
        self.left_encoder_value = 0

    def update(self):
        self.linear_speed = (self.right_speed + self.left_speed)/2
        self.angular_speed = (self.right_speed - self.left_speed)/WHEEL_DIST
        print("\nAngular: ", self.right_speed, self.left_speed, self.angular_speed)

        elapsed_time = self.system_clock.get_elapsed_time_since_last_call(self.clock_id)

        # Update encoders
        self.right_encoder_value += abs(self.right_speed * elapsed_time)
        self.left_encoder_value += abs(self.left_speed * elapsed_time)

        # Update position
        self.theta += self.angular_speed * elapsed_time 
        self.theta %= 2*pi
        self.x += self.linear_speed * cos(self.theta) * elapsed_time 
        self.y += self.linear_speed * sin(self.theta) * elapsed_time 
        # Will we update the ultrassound distance in simulation? 