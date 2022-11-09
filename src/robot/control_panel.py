class ControlPanel:
    '''
    ControlPanel implements variables that are never changed nor measured by the robot, 
    but rather imposedby the administrator. For instance, they can be received through 
    the network module.'''
    def __init__(self, should_run):
        self.run = should_run
        self.target = (0, 0)
        self.reset_flag = False
    
    def set_target(self, x, y):
        self.target = (x, y)

    def reset_state(self, x, y, theta):
        self.reset_flag = True
        self.reset_values = (x, y, theta)
    
    def print(self):
        print("Running =", self.run, " target = ", self.target)