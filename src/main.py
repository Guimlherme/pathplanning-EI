from perception import Sensors, State
from decision_making import DecisionMaking

class Robot:
    def __init__(self, sensors, decision_making):
        self.sensors = sensors
        self.decision_making = decision_making
        self.state = State()
    
    def run(self):
        while True:
            perception = self.sensors.collect()
            self.state.update(perception)
            command = self.decision_making.decide(self.state, perception)
            command.execute()


sensors = Sensors(debug=True)
decision_making = DecisionMaking(debug=True)
robot = Robot(sensors, decision_making)

robot.run()
            