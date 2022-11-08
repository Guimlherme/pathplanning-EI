class ControlPanel:
    '''
    ControlPanel implements variables that are never changed nor measured by the robot, 
    but rather imposedby the administrator. For instance, they can be received through 
    the network module.'''
    def __init__(self):
        self.run = False
        self.target = (0, 0)
    
    def set_target(self, x, y):
        self.target = (x, y)
    
    def print(self):
        print("Running =", self.run, " target = ", self.target)