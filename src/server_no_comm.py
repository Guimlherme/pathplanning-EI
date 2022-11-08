from perception import MockSensors, State, Map
from decision_making import DecisionMaking
from communication import Network
from threading import Thread
from robot import ControlPanel, Robot

# Build world map
world_map = Map()
world_map.add_node(0, 0, 0)
world_map.add_node(1, 1, 0)
world_map.add_edge(0, 1)

# Build sensors and decision making
sensors = MockSensors(debug=True)
decision_making = DecisionMaking(debug=True)

# Instantiate the robot
robot = Robot(sensors, decision_making, world_map)

# Listen to network communication
control_panel = ControlPanel()
control_panel.run = True

# Main loop
while True:
    if control_panel.run:
        robot.run()
    
network_thread.join()
           