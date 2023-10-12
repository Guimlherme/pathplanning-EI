from command import Actuator
from constants import OMEGA_MAX, WHEEL_RADIUS

class MockActuators(Actuator):
    def __init__(self, simulation) -> None:
        super().__init__()
        self.simulation = simulation

    def set_speeds(self, right_speed, left_speed):
        # Saves speeds as m/s
        self.simulation.right_speed = right_speed * OMEGA_MAX * WHEEL_RADIUS
        self.simulation.left_speed = left_speed * OMEGA_MAX * WHEEL_RADIUS