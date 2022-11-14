from perception import State, Sensing
from communication import Network
from threading import Thread
from robot import ControlPanel, Robot
from config import Configs
from clock import SystemClock
from command import CommandFactory
from maps import get_trivial_map, get_grid_map, get_quarto_map
from decision_making import SimpleDecisionMaking, GridDecisionMaking

from infrastructure.mock import MockSensors, MockActuators, Simulation

import argparse

# Parse flags
parser = argparse.ArgumentParser(
    prog = 'AutoSync Server',
    description = 'Server for autosync robot.')
parser.add_argument('-r', '--run', action='store_true')
parser.add_argument('-m', '--mock', action='store_true')
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('-l', '--log', action='store_true')
parser.add_argument('-a', '--host')
parser.add_argument('-dm', '--decision_making')
args = parser.parse_args()

debug = args.debug
should_run = args.run

configs = Configs()
if args.host is not None:
    configs.set_setting("host", args.host)

# Build world map
world_map = get_grid_map()

# Build control panel and system clock
control_panel = ControlPanel(should_run)
system_clock = SystemClock()

# Build sensors and actuators
if args.mock:
    simulation = Simulation(system_clock)
    simulation.add_obstacle(100, 100)
    simulation.add_obstacle(200, 200)
    simulation.add_obstacle(300, 100)
    sensors = MockSensors(system_clock, simulation, debug=debug)
    actuators = MockActuators(simulation)
else:
    simulation = None
    from infrastructure.arduino import Arduino, ArduinoSensors, ArduinoActuators
    arduino = Arduino()
    arduino.connect()
    actuators = ArduinoActuators(arduino)
    sensors = ArduinoSensors(arduino, debug=debug)

# Build remaining dependencies
command_factory = CommandFactory(actuators, simulation=args.mock)
sensing = Sensing(sensors, system_clock, debug=True)
network = Network(control_panel, configs)

if args.decision_making == 'simple':
    decision_making = SimpleDecisionMaking(command_factory, debug=debug)
elif args.decision_making == 'grid':
    decision_making = GridDecisionMaking(command_factory, debug=debug)
else: # defaults to grid
    decision_making = GridDecisionMaking(command_factory, debug=debug)


# Instantiate the robot
robot = Robot(sensing, decision_making, world_map, control_panel, system_clock, network, command_factory, simulation, debug=debug, log=args.log)
robot.run()
           