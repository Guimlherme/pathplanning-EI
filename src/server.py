from perception import MockSensors, State, Map
from decision_making import DecisionMaking
from communication import Network
from threading import Thread
from robot import ControlPanel, Robot

from infrastructure import ArduinoSensors

import argparse

# Parse flag
parser = argparse.ArgumentParser(
    prog = 'AutoSync Server',
    description = 'Server for autosync robot.')
parser.add_argument('-nn', '--no_network', action='store_true')
parser.add_argument('-m', '--mock', action='store_true')
args = parser.parse_args()

# Build world map
world_map = Map()
world_map.add_node(0, 0, 0)
world_map.add_node(1, 1, 0)
world_map.add_edge(0, 1)

# Build sensors and decision making
sensors = MockSensors(debug=True)
if not args.mock:
    sensors = ArduinoSensors(debug=True)

decision_making = DecisionMaking(debug=True)

# Instantiate the robot
robot = Robot(sensors, decision_making, world_map)

# Listen to network communication
control_panel = ControlPanel()

if args.no_network:
    control_panel.run = True
else:
    network = Network(control_panel)
    network_thread = Thread(target=network.read)
    network_thread.start()

# Main loop
while True:
    if control_panel.run:
        robot.run()

# Finalizing
if not args.no_network:
    network_thread.join()
           