import numpy as np 
import time

class MockSensors:
    def __init__(self, system_clock, debug=False):
        self.debug = debug
        self.system_clock = system_clock
        self.clock_id = system_clock.get_id()

    def camera_shot(self):
        time.sleep(0.5)
        elapsed_time = self.system_clock.get_elapsed_time_since_last_call(self.clock_id)
        # print("Elapsed time since last camera update: %.3f ms" % (1000*elapsed_time)) 
        image = np.zeros((64, 64, 3), np.uint8)
        image[:, 30:32, :] = 1
        return image


    def right_encoder(self):
        return 0.5

    def left_encoder(self):
        return 0.5

    def ultrassound_distance(self):
        return 0.4
