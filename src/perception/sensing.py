from .perception import Perception
from .preprocessing_image import preprocessing_image

class Sensing:
    def __init__(self, sensors, debug=False):
        self.sensors = sensors
        self.debug = debug

    def collect(self, perception):
        if self.debug:
            print("Collecting from sensors")

        right_encoder = self.sensors.right_encoder()
        left_encoder = self.sensors.left_encoder()

        linear_speed = right_encoder # TODO: change
        angular_speed = right_encoder # TODO: change
        object_distance = self.sensors.ultrassound_distance()

        perception.set_angular_speed(angular_speed)
        perception.set_linear_speed(linear_speed)
        perception.set_obstacle_distance(object_distance)

    def collect_vision(self, perception):
        # print("Collecting from vision")
            
        image = self.sensors.camera_shot()
        line_angle = preprocessing_image(image)
        perception.set_line_angle(line_angle)