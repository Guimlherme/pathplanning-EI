from perception import Sensors, State, Map

class Robot:
    def __init__(self, sensors, decision_making, world_map):
        self.sensors = sensors
        self.decision_making = decision_making
        self.state = State(world_map)
    
    def run(self):
        perception = self.sensors.collect()
        self.state.update(perception)
        command = self.decision_making.decide(self.state, perception)
        command.execute()
