class Actuator:
    def set_speeds(self, left, right):
        raise Exception('Abstract Actuator cannot set speeds')