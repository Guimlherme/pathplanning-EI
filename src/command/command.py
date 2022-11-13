RIGHT = 1
LEFT = -1
from constants import WHEEL_RADIUS,ROBOT_SPEED,ROBOT_WIDTH,OMEGA_MAX,CONTROL_PARAMETERS,OMEGA_NON_LINEAR
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
        
        # Need for non-linear interpolation
        self.yp_left = [0.0, 1.193805, 2.513274, 3.455752, 4.335398,5.529203,
                        6.09469, 6.78584, 7.476991, 8.419468,8.859291,9.801769,
                        10.430088, 10.995574, 11.812388, 12.189379, 12.377875,13.006194]

        self.yp_right = [0.0, 0.376991, 2.638938, 3.832743, 4.838053, 5.78053, 6.471681,
                         7.162831, 7.539822, 7.853982, 8.293805, 8.356636, 8.607964,
                         8.796459, 8.796459, 9.047787, 9.48761, 9.990265]

        self.xp = [.10, .20, .25, .30, .35, .40, .45, .50, .55, .60, .65, .70, .75, .80, .85, .90, .95, 1.00]

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
                
        if w_left > OMEGA_NON_LINEAR or w_right > OMEGA_NON_LINEAR:
            w_left = OMEGA_MAX * np.interp([w_left],self.xp,self.yp_left)[0]
            w_right = OMEGA_MAX * np.interp([w_right],self.xp,self.yp_right)[0]
                
        state.right_wheel_command = w_right
        state.left_wheel_command = w_left
        print("Left wheel speed: ", w_left)
        print("Right wheel speed: ", w_right)
        self.actuators.set_speeds(w_right / (OMEGA_MAX), w_left / (OMEGA_MAX))
    
    def get_name(self):
        return "Forward"
