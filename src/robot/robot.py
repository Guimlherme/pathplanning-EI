from perception import State, Map, Perception
from threading import Thread
import time

CYCLE_TIME = 0.015 #in seconds

class Robot:
    def __init__(self, sensing, decision_making, world_map, control_panel, system_clock, network):
        self.sensing = sensing
        self.decision_making = decision_making
        self.state = State(world_map, control_panel, system_clock, debug=True)
        self.control_panel = control_panel
        self.perception = Perception(0, 0, 0, 0)
        self.shutdown = False
        self.system_clock = system_clock
        self.network = network
    
    def run(self):
        vision_thread = Thread(target=self.run_vision)
        network_thread = Thread(target=self.network.read)
        remaining_thread = Thread(target=self.run_everything)

        vision_thread.start()
        network_thread.start()
        remaining_thread.start()

        self._wait([vision_thread, network_thread, remaining_thread])

    def _wait(self, threads):
        try:
            while 1:
                time.sleep(.1)
        except KeyboardInterrupt:
            print("attempting to close threads")
            self.shutdown = True
            self.network.shutdown = True
            for thread in threads:
                thread.join()
            print ("threads successfully closed")

    def run_vision(self):
        while not self.shutdown:
            self.sensing.collect_vision(self.perception)
    
    def run_everything(self):
        clock_id = self.system_clock.get_id()
        while not self.shutdown:
            _ = self.system_clock.get_elapsed_time_since_last_call(clock_id) # mark first call
            if self.control_panel.run:
                self.execute_cycle()
            elapsed_time = self.system_clock.get_elapsed_time_since_last_call(clock_id) # get elapsed time
            remaining_time = CYCLE_TIME - elapsed_time
            if remaining_time > 0:
                time.sleep(remaining_time)

    def execute_cycle(self):
        self.sensing.collect(self.perception)
        self.state.update(self.perception)
        command = self.decision_making.decide(self.state, self.control_panel.target, self.perception)
        command.execute()