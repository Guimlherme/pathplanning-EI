import time

class SystemClock:
    def __init__(self):
        self.last_id = 0
        self.timers = { }
    
    def get_id(self):
        self.last_id += 1
        self.timers[self.last_id] = time.time()
        return self.last_id
    
    def get_elapsed_time_since_last_call(self, id):
        current_time = time.time()
        previous_time = self.timers[id]
        elapsed_time = current_time - previous_time
        self.timers[id] = current_time
        return elapsed_time