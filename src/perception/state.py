from .perception import Perception

TIMESTEP = 60e-3 #60ms

class State:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0

    def update(self, perception : Perception) -> None:
        self.x += perception.speed * TIMESTEP 
        self.y += perception.speed * TIMESTEP 
    
    def found_target(self) -> bool:
        return True
    
    def object_detected(self) -> bool:
        return False