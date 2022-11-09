from .perception import Perception
import numpy as np 
import cv2 
class MockSensors:
    def __init__(self, debug=False):
        self.debug = debug

    def camera_shot(self):
        image = np.zeros((64, 64, 3), np.uint8)
        image[:, 30:32, :] = 1
        return image


    def right_encoder(self):
        return 0.5

    def left_encoder(self):
        return 0.5

    def ultrassound_distance(self):
        return 0.4
