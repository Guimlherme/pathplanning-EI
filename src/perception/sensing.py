class Sensing:
    def __init__(self, sensors, system_clock, debug=False):
        self.sensors = sensors
        self.debug = debug

    def collect(self):
        print("A1")
        right_encoder = self.sensors.right_encoder()
        print("A2")
        left_encoder = self.sensors.left_encoder()
        print("A3")
        # object_distance = self.sensors.ultrassound_distance()
        object_distance = 100
        return right_encoder, left_encoder, object_distance

    def collect_vision(self):            
        image = self.sensors.camera_shot()
        return image