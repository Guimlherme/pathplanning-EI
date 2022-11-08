from perception import Sensors, State, Map

class Robot:
    def __init__(self, sensors, decision_making, world_map, control_panel):
        self.sensors = sensors
        self.decision_making = decision_making
        self.state = State(world_map)
        self.control_panel = control_panel
    
    def run(self):
        perception = self.sensors.collect()
        self.state.update(perception)
        command = self.decision_making.decide(self.state, self.control_panel.target, perception)
        command.execute()
