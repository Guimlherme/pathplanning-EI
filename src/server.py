from perception import State, Sensing
from decision_making.simple import DecisionMaking
from communication import Network
from threading import Thread
from robot import ControlPanel, Robot
from config import Configs
from clock import SystemClock
from command import CommandFactory
from maps import get_trivial_map, get_grid_map

from infrastructure.arduino import Arduino, ArduinoSensors, ArduinoActuators
from infrastructure.mock import MockSensors, MockActuators

import argparse

# Parse flags
parser = argparse.ArgumentParser(
    prog = 'AutoSync Server',
    description = 'Server for autosync robot.')
parser.add_argument('-r', '--run', action='store_true')
parser.add_argument('-m', '--mock', action='store_true')
parser.add_argument('-d', '--debug', action='store_true')
args = parser.parse_args()

debug = args.debug
should_run = args.run

configs = Configs()

# Build world map
world_map = get_trivial_map()

# Build control panel and system clock
control_panel = ControlPanel(should_run)
system_clock = SystemClock()

# Build sensors and actuators
sensors = MockSensors(system_clock, debug=debug)
actuators = MockActuators()
if not args.mock:
    arduino = Arduino()
    arduino.connect()
    actuators = ArduinoActuators(arduino)
    sensors = ArduinoSensors(arduino, debug=debug)

# Build remaining dependencies
command_factory = CommandFactory(actuators)
sensing = Sensing(sensors, system_clock, debug=True)
decision_making = DecisionMaking(command_factory, debug=debug)
network = Network(control_panel, configs)

# Instantiate the robot
robot = Robot(sensing, decision_making, world_map, control_panel, system_clock, network, command_factory)
robot.run()
           