from perception import State, Map, Sensing
from decision_making import DecisionMaking, SimpleDecisionMaking
from communication import Network
from threading import Thread
from robot import ControlPanel, Robot
from config import Configs
from clock import SystemClock
from command import CommandFactory

from infrastructure import Arduino, ArduinoSensors, ArduinoActuators
from infrastructure.mock import MockSensors, MockActuators

import argparse

# Parse flag
parser = argparse.ArgumentParser(
    prog = 'AutoSync Server',
    description = 'Server for autosync robot.')
parser.add_argument('-nn', '--no_network', action='store_true')
parser.add_argument('-m', '--mock', action='store_true')
parser.add_argument('-d', '--debug', action='store_true')
args = parser.parse_args()

configs = Configs()

# Build world map
world_map = Map()
world_map.add_node(0, 0, 0)
world_map.add_node(1, 1, 0)
world_map.add_edge(0, 1)

debug = args.debug
# Build sensors and decision making
control_panel = ControlPanel()
system_clock = SystemClock()

sensors = MockSensors(system_clock, debug=debug)
actuators = MockActuators()
if not args.mock:
    arduino = Arduino()
    arduino.connect()
    actuators = ArduinoActuator(arduino)
    sensors = ArduinoSensors(arduino, debug=debug)

command_factory = CommandFactory(actuators)
sensing = Sensing(sensors)
decision_making = SimpleDecisionMaking(command_factory, debug=debug)

# Instantiate the robot
robot = Robot(sensing, decision_making, world_map, control_panel, system_clock)

# Listen to network communication
if args.no_network:
    control_panel.run = True
else:
    network = Network(control_panel, configs)
    network_thread = Thread(target=network.read)
    network_thread.start()

# Main loop
robot.run()

# Finalizing
if not args.no_network:
    network_thread.join()
           