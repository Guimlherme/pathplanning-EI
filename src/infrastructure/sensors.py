import perception

class ArduinoSensors:
    def __init__(self, debug=False):
        self.debug = debug

    def collect(self) -> perception.Perception:
        if self.debug:
            print("Collecting from sensors")
        
        angle = 0 # TODO get from the camera
        linear_speed = 1 
        angular_speed = 1
        obstacle_distance = 1
        return perception.Perception(angle, linear_speed, angular_speed, obstacle_distance)