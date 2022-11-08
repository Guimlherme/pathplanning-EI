from control import Stopped, HalfTurn, Forward, Command

class DecisionMaking:
    def __init__(self, debug=False):
        self.debug = debug

    def decide(self, state, perception) -> Command:
        if self.debug:
            print("Running decision making")

        if state.found_target():
            command = Stopped()
        elif state.object_detected():
            command = HalfTurn()
        else:
            # follow line
            command = Forward(perception.line_angle)
            # TODO: what if there is more than one angle? path planning

        if self.debug:
            print("Decided command", command.get_name())
        return command