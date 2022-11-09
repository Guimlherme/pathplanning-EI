from perception import State, Map

class Robot:
    def __init__(self, sensing, decision_making, world_map, control_panel, system_clock):
        self.sensing = sensing
        self.decision_making = decision_making
        self.state = State(world_map, control_panel, system_clock, debug=True)
        self.control_panel = control_panel
    
    def run(self):
        perception = self.sensing.collect()
        self.state.update(perception)
        command = self.decision_making.decide(self.state, self.control_panel.target, perception)
        command.execute()

