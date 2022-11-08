from perception import MockSensors, State, Map
from decision_making import DecisionMaking
from communication import Network
from control import MockCommandFactory
from threading import Thread
from robot import ControlPanel, Robot
from config import Configs

from infrastructure import ArduinoSensors, ArduinoCommandFactory, Arduino

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

sensors = MockSensors(debug=debug)
command_factory = MockCommandFactory()
if not args.mock:
    arduino = Arduino()
    sensors = ArduinoSensors(arduino, debug=debug)
    command_factory = ArduinoCommandFactory(arduino, debug=debug)

decision_making = DecisionMaking(command_factory, debug=debug)

# Instantiate the robot
robot = Robot(sensors, decision_making, world_map, control_panel)

# Listen to network communication
if args.no_network:
    control_panel.run = True
else:
    network = Network(control_panel, configs)
    network_thread = Thread(target=network.read)
    network_thread.start()

# Main loop
count = 0
while True:
    if count == 100:
        control_panel.print()
        count = 0
    if control_panel.run:
        robot.run()
    count += 1

# Finalizing
if not args.no_network:
    network_thread.join()
           