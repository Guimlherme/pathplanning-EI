import numpy as np

CYCLE_TIME = 15e-3 # s
DISTANCE_THRESHOLD = 15 # cm
FINISH_TURN_ANGLE_THRESHOLD = np.deg2rad(15) # rad
TURN_ANGLE_THRESHOLD = np.deg2rad(35)

WHEEL_DIST = 15.2 # centimeters

ROBOT_WIDTH = 0.152 # m
ROBOT_SPEED = 0.22 # m/s
WHEEL_RADIUS = 0.0325 # m
OMEGA_MAX = 10.00 # rad/s

# CONTROL LAW PARAMETERS
XI = 0.70
WN = 6.00      # rad/s
TAU = 0.600    # s
TD = 0.060     # s - time of discretization

CONTROL_PARAMETERS = {
     'phi':{'k':(2*(TAU-TD)*(WN**2))/(4+TD*WN*(4*XI+TAU*WN)),
            'k-1':-(2*(TAU+TD)*(WN**2))/(4+TD*WN*(4*XI+TAU*WN))},
     'u':{'k-1':(4-TD*WN*(4*XI+TAU*WN))/(4+TD*WN*(4*XI+TAU*WN))},
}
