class DecisionMaking:
    def __init__(self, command_factory, debug=False):
        self.command_factory = command_factory
        self.debug = debug

    def decide(self, state, target, perception):
        if self.debug:
            print("Running decision making")

        if state.position_is(target):
            command = self.command_factory.stopped()
        elif state.obstacle_detected:
            command = self.command_factory.half_turn()
        elif state.intersection_detected():
            # TODO: decide next location (path planning) and make a left or right turn
            command = self.command_factory.forward(perception.line_angle)
        else:
            command = self.command_factory.forward(perception.line_angle)

        if self.debug:
            print("Decided command", command.get_name())
        return command