import numpy as np
import command
from math import pi

# SimpleDecisionMaking only go forward and does a half turn when finds an obstacle. Ignores intersection and path planning
class DecisionMaking:
    def __init__(self, command_factory, debug=False):
        self.command_factory = command_factory
        self.debug = debug
        self.current_state = StoppedState(command_factory)

    def decide(self, state, target, target_node, perception):
        command = self.current_state.execute(state, target, perception)
        next_state = self.current_state.check_transition(state, target, perception)
        if next_state is not None:
            self.current_state = next_state

        if self.debug:
            print("Decision Making:", command.get_name())
        return command

class ForwardState:
    def __init__(self, command_factory):
        self.command_factory = command_factory

    def execute(self, state, target, perception):
        return self.command_factory.forward(perception.line_angle)

    def check_transition(self, state, target, perception):
        if state.position_is(target):
            return StoppedState(self.command_factory)
        elif state.obstacle_detected:
            return TurnState(self.command_factory, state, np.deg2rad(90))
        return None

class StoppedState:
    def __init__(self, command_factory):
        self.command_factory = command_factory
        
    def execute(self, state, target, perception):
        return self.command_factory.stopped()
        
    def check_transition(self, state, target, perception):
        if not state.position_is(target):
            return ForwardState(self.command_factory)
        return None

class TurnState:
    def __init__(self, command_factory, state, angle):
        self.angle = angle
        self.initial_theta = state.theta
        self.command_factory = command_factory

        self.finished_turning = False

    def execute(self, state, target, perception):
        return self.command_factory.turn(command.RIGHT)

    def check_transition(self, state, target, perception):
        if angle_diference(state.theta, self.initial_theta)  < np.deg2rad(10):
            self.finished_turning = True
        if self.finished_turning and not state.obstacle_detected:
            return ForwardState(self.command_factory)
        return None

def angle_diference(x, y):
    diff = y - x
    return min ( diff % (2*pi), (- diff) % (2*pi))
