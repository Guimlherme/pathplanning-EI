import numpy as np 
import time
from math import floor

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
        return self.simulation.distance
