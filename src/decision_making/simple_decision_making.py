import numpy as np

# SimpleDecisionMaking only go forward and does a half turn when finds an obstacle. Ignores intersection and path planning
class SimpleDecisionMaking:
    def __init__(self, command_factory, debug=False):
        self.command_factory = command_factory
        self.debug = debug

    def decide(self, state, target, perception):
        if state.position_is(target):
            command = self.command_factory.stopped()
        elif state.obstacle_detected:
            command = self.command_factory.half_turn()
        else:
            command = self.command_factory.forward(perception.line_angle)

        if self.debug:
            print("Decision Making:", command.get_name())
        return command