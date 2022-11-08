from .perception import Perception

class Sensors:
    def __init__(self, debug=False):
        self.debug = debug

    def collect(self) -> Perception:
        if self.debug:
            print("Collecting from sensors")
        return Perception(0.5, 0.5, 0.5)