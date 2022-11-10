RIGHT = 1
LEFT = -1
from constants import WHEEL_RADIUS,ROBOT_SPEED,ROBOT_WIDTH,OMEGA_MAX,CONTROL_PARAMETERS
import numpy as np

class Command:
    def get_name(self):
        return "Abstract Command"

    def execute(self, state):
        raise Exception('Abstract Command cannot be executed')

class Stopped(Command):
    def __init__(self, actuators):
        self.actuators = actuators

    def execute(self, state):
        state.right_wheel_command = 0
        state.left_wheel_command = 0
        self.actuators.set_speeds(0, 0)
    
    def get_name(self):
        return "Stopped"

class LeftTurn(Command):
    def __init__(self, actuators):
        self.actuators = actuators

    def execute(self, state):
        state.right_wheel_command = 1
        state.left_wheel_command = -1
        self.actuators.set_speeds(1, -1)

    def get_name(self):
        return "LeftTurn"

class RightTurn(Command):
    def __init__(self, actuators):
        self.actuators = actuators

    def execute(self, state):
        state.right_wheel_command = -1
        state.left_wheel_command = 1
        self.actuators.set_speeds(-1, 1)

    def get_name(self):
        return "RightTurn"


class Forward(Command):

    def __init__(self, actuators):
        self.actuators = actuators
        self.command = 0

    def execute(self, state):

        privious_command = self.command
        phi = state.line_angle
        previous_phi= state.previous_line_angle

        u  = CONTROL_PARAMETERS['u']['k-1']*privious_command
        u += CONTROL_PARAMETERS['phi']['k']*phi 
        u += CONTROL_PARAMETERS['phi']['k-1']*previous_phi

        self.command = u

        if u > 0:
            w_right = (ROBOT_SPEED+((ROBOT_WIDTH/2)*u))/WHEEL_RADIUS
            w_left = (ROBOT_SPEED-((ROBOT_WIDTH/2)*u))/WHEEL_RADIUS

            if w_right > OMEGA_MAX:
                w_right = OMEGA_MAX
                w_left = 2*(1/WHEEL_RADIUS)*(ROBOT_SPEED) - (OMEGA_MAX)
        else:
            u = np.abs(u)
            w_right = (ROBOT_SPEED-((ROBOT_WIDTH/2)*u))/WHEEL_RADIUS
            w_left = (ROBOT_SPEED+((ROBOT_WIDTH/2)*u))/WHEEL_RADIUS

            if w_left > OMEGA_MAX:
                w_left = OMEGA_MAX
                w_right = 2*(1/WHEEL_RADIUS)*(ROBOT_SPEED) - (OMEGA_MAX)
                
        state.right_wheel_command = w_right
        state.left_wheel_command = w_left
        print("Left wheel speed: ", w_left)
        print("Right wheel speed: ", w_right)
        self.actuators.set_speeds(w_right / (OMEGA_MAX+1.3), w_left / (OMEGA_MAX+1.3))
    
    def get_name(self):
        return "Forward"
