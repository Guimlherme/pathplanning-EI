RIGHT = 1
LEFT = -1
from constants import WHEEL_RADIUS,ROBOT_SPEED_MAX,ROBOT_WIDTH,OMEGA_MAX,CONTROL_PARAMETERS,DEL_SPEED_DEL_PSI
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

    def __init__(self, actuators, simulation=False):
        self.actuators = actuators
        self.command = 0
        
        # Need for non-linear interpolation
        self.xp_left = [0.0, 1.193805, 2.513274, 3.455752, 4.335398,5.529203,
                        6.09469, 6.78584, 7.476991, 8.419468,8.859291,9.801769,
                        10.430088, 10.995574, 11.812388, 12.189379, 12.377875,13.006194]

        self.xp_right = [0.0, 0.376991, 2.638938, 3.832743, 4.838053, 5.78053, 6.471681,
                         7.162831, 7.539822, 7.853982, 8.293805, 8.356636, 8.607964,
                         8.796459, 8.796459, 9.047787, 9.48761, 9.990265]

        self.yp = [0.10, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55,
                   0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
        
        self.speed = ROBOT_SPEED_MAX
        self.simulation = simulation
        
    def update_speed(self,psi):
        return ROBOT_SPEED_MAX - DEL_SPEED_DEL_PSI*np.abs(psi)

    def execute(self, state):

        privious_command = self.command
        psi = state.line_angle
        previous_psi= state.previous_line_angle

        u  = CONTROL_PARAMETERS['u']['k-1']*privious_command
        u += CONTROL_PARAMETERS['phi']['k']*psi 
        u += CONTROL_PARAMETERS['phi']['k-1']*previous_psi

        self.command = u
        self.speed = self.update_speed(psi)

        if u > 0:
            w_right = (self.speed+((ROBOT_WIDTH/2)*u))/WHEEL_RADIUS
            w_left = (self.speed-((ROBOT_WIDTH/2)*u))/WHEEL_RADIUS

            if w_right > OMEGA_MAX:
                w_right = OMEGA_MAX
                w_left = 2*(1/WHEEL_RADIUS)*(self.speed) - (OMEGA_MAX)
        else:
            u = np.abs(u)
            w_right = (self.speed-((ROBOT_WIDTH/2)*u))/WHEEL_RADIUS
            w_left = (self.speed+((ROBOT_WIDTH/2)*u))/WHEEL_RADIUS

            if w_left > OMEGA_MAX:
                w_left = OMEGA_MAX
                w_right = 2*(1/WHEEL_RADIUS)*(self.speed) - (OMEGA_MAX)
                

        if self.simulation:
            w_right = 1
            w_left = 1
        else:
            w_left = np.interp(w_left,self.xp_left,self.yp)
            w_right = np.interp(w_right,self.xp_right,self.yp)

        state.right_wheel_command = w_right
        state.left_wheel_command = w_left
        print("Left wheel speed: ", w_left)
        print("Right wheel speed: ", w_right)
        self.actuators.set_speeds(w_right, w_left)
    
    def get_name(self):
        return "Forward"
