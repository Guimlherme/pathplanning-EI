from .perception import Perception
from .preprocessing_image import preprocessing_image

class Sensing:
    def __init__(self, sensors, debug=False):
        self.sensors = sensors
        self.debug = debug

    def collect(self) -> Perception:
        if self.debug:
            print("Collecting from sensors")
        
        image = self.sensors.camera_shot()
        line_angle = preprocessing_image(image)

        right_encoder = self.sensors.right_encoder()
        left_encoder = self.sensors.left_encoder()

        linear_speed = right_encoder # TODO: change
        angular_speed = right_encoder # TODO: change

        object_distance = self.sensors.ultrassound_distance()

        return Perception(line_angle, linear_speed, angular_speed, object_distance)