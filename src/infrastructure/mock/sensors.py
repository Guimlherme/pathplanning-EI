import numpy as np 
import time
from math import floor, tan, sqrt, atan2, pi

class MockSensors:
    def __init__(self, system_clock, simulation, debug=False):
        self.debug = debug
        self.system_clock = system_clock
        self.clock_id = system_clock.get_id()
        self.simulation = simulation

    def camera_shot(self):
        time.sleep(0.5)
        image = np.zeros((64, 64, 3), np.uint8)
        image[:, 30:32, :] = 1
        return image

    # Return values in int centimeters
    def right_encoder(self):
        return floor(self.simulation.right_encoder_value * 100)

    def left_encoder(self):
        return floor(self.simulation.left_encoder_value * 100)

    def ultrassound_distance(self):
        # Update ultrassound distance
        # 1. Detect objects in front of the robot.
        #   a. Distance from each object to line of robot < 3m
        #   b. Robot-object vector is in same orientation as the robot 

        # line of the robot is y = y1 + m (x-x1) or mx - y + (y1-mx1) = 0
        m = tan(self.simulation.theta)
        A = m
        B = -1
        C = self.simulation.y - m*self.simulation.x

        aligned_objects = []
        for i, obj in enumerate(self.simulation.obstacle_positions):
            dist = abs(A*obj[0] + B*obj[1] + C) / sqrt(A**2 + B**2)

            robot_position = np.array([self.simulation.x, self.simulation.y])
            robot_to_object = np.array(obj) - robot_position
            robot_to_object_angle = atan2(robot_to_object[1], robot_to_object[0])

            angle = angle_diference(robot_to_object_angle, self.simulation.theta)
            print("Obstacle ", i, "distance", dist, "angle", angle)
            print("Position ", obj, " m ", m, "A", A, "B", B)
            print("Theta used", self.simulation.theta)

            if dist < 10 and angle < np.deg2rad(90):
                aligned_objects.append(obj)

        if len(aligned_objects) == 0:
            return 99999

        # 3. Get the closest object
        # OBS: Using Euclidian distance, ideally would get distance in the robot vision line 
        # (distance to projection instead of distance to point)
        minimum_distance = sqrt((aligned_objects[0][0] - self.simulation.x) ** 2 + (aligned_objects[0][1] - self.simulation.y) ** 2)
        for obj in aligned_objects:
            distance = sqrt((obj[0] - self.simulation.x) ** 2 + (obj[1] - self.simulation.y) ** 2)
            if distance < minimum_distance:
                minimum_distance = distance

        return minimum_distance

def angle_diference(x, y):
    diff = y - x
    return min ( diff % (2*pi), (- diff) % (2*pi))

