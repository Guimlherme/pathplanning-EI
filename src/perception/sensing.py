from .perception import Perception
from .preprocessing_image import preprocessing_image

WHEEL_DIST = 15 # centimeters

class Sensing:
    def __init__(self, sensors, system_clock, debug=False):
        self.sensors = sensors
        self.debug = debug

        self.system_clock = system_clock
        self.clock_id = system_clock.get_id()

        self.right_encoder_previous = 0
        self.left_encoder_previous = 0

    def collect(self, perception):
        elapsed_time = self.system_clock.get_elapsed_time_since_last_call(self.clock_id)

        right_encoder = self.sensors.right_encoder()
        left_encoder = self.sensors.left_encoder()

        right_speed = (right_encoder - self.right_encoder_previous)/elapsed_time
        left_speed = (left_encoder - self.left_encoder_previous)/elapsed_time

        self.right_encoder_previous = right_encoder
        self.left_encoder_previous = left_encoder

        linear_speed = (right_speed + left_speed)/2
        angular_speed = (right_speed - left_speed)/WHEEL_DIST

        object_distance = self.sensors.ultrassound_distance()

        perception.set_angular_speed(angular_speed)
        perception.set_linear_speed(linear_speed)
        perception.set_obstacle_distance(object_distance)
        if self.debug:
            print("Encoders: ", right_encoder, left_encoder)
            print("Wheel Speeds: ", right_speed, left_speed)
            print("Linear and angular Speeds: ", linear_speed, angular_speed)

    def collect_vision(self, perception):
        # print("Collecting from vision")
            
        image = self.sensors.camera_shot()
        line_angle = preprocessing_image(image)
        perception.set_line_angle(line_angle)