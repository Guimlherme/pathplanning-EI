import inspect
from perception import State, Map
from threading import Thread, Lock
import time
import ctypes
import json
from constants import CYCLE_TIME, CONTROL_TIME

class Robot:
    def __init__(self, sensing, decision_making, world_map, control_panel, system_clock, network, command_factory, debug=True):
        self.sensing = sensing
        self.decision_making = decision_making
        self.state = State(world_map, control_panel, system_clock, debug=True)
        self.control_panel = control_panel
        self.shutdown = False
        self.system_clock = system_clock
        self.network = network
        self.command_factory = command_factory
        self.control_clock_id = system_clock.get_id()
        self.control_external_clock_id = system_clock.get_id()

        self.target = (0, 0)
        self.target_node = 0

        self.control_lock = Lock()

        self.debug = debug
        if self.debug:
            self.reset_history()
    
    def reset_history(self):
        self.history = {
                'x': [], 'y': [], 'theta': [], 
                'linear_speed': [], 'angular_speed': [], 'object_distance': [],   
                'localization_elapsed_time': [], 'vision_elapsed_time': [], 'control_elapsed_time': [],
                'next_waypoint': [], 'current_state': [], 
        }

    def run(self):
        vision_thread = Thread(target=self.run_vision)
        network_thread = Thread(target=self.network.read)
        remaining_thread = Thread(target=self.run_everything)
        control_thread = Thread(target=self.run_control)

        vision_thread.start()
        network_thread.start()
        remaining_thread.start()
        control_thread.start()

        self._wait([vision_thread, network_thread, remaining_thread, control_thread])

    def _wait(self, threads):
        try:
            while 1:
                time.sleep(.1)
        except KeyboardInterrupt:
            print("attempting to close threads")
            self.shutdown = True
            self.network.close()
            for thread in threads:
                thread.join()
            print ("threads successfully closed")

    def run_vision(self):
        while not self.shutdown:
            image = self.sensing.collect_vision( )
            self.state.update_vision(image)
    
    def run_everything(self):
        clock_id = self.system_clock.get_id()
        while not self.shutdown:
            _ = self.system_clock.get_elapsed_time_since_last_call(clock_id) # mark first call
            if self.control_panel.run:
                print("Run: True")
                self.execute_cycle()
            else:
                print("Run: False")
                with self.control_lock:
                    self.command = self.command_factory.stopped()
                if len(self.history['x']) > 0:
                    with open('log.txt', 'w') as logfile:
                        logfile.write(json.dumps(self.history))
                    self.reset_history()
                
            elapsed_time = self.system_clock.get_elapsed_time_since_last_call(clock_id) # get elapsed time
            remaining_time = CYCLE_TIME - elapsed_time
            if remaining_time > 0:
                print("Going to sleep for", remaining_time)
                time.sleep(remaining_time)

    def execute_cycle(self):
        if self.control_panel.target != self.target:
            self.target = self.control_panel.target
            self.target_node = self.state.world_map.get_closest_node(self.target[0], self.target[1])

        print("A")
        right_encoder, left_encoder, obstacle_distance = self.sensing.collect()
        print("B")
        self.state.update_from_sensors(right_encoder, left_encoder, obstacle_distance)
        print("C")
        command = self.decision_making.decide(self.state, self.target, self.target_node)
        print("D")
        with self.control_lock:
            print("E")
            self.command = command
        print("F")
        if self.debug:
            self.history['x'].append(self.state.x)
            self.history['y'].append(self.state.y)
            self.history['theta'].append(self.state.theta)
            self.history['linear_speed'].append(self.state.linear_speed)
            self.history['angular_speed'].append(self.state.angular_speed)
            self.history['localization_elapsed_time'].append(self.state.localization_elapsed_time)
            self.history['vision_elapsed_time'].append(self.state.vision_elapsed_time)
            self.history['object_distance'].append(self.state.obstacle_distance)
            self.history['next_waypoint'].append(self.decision_making.next_waypoint)
            self.history['current_state'].append(self.decision_making.current_state.get_name())
        print("G")

    def run_control(self):
        while not self.shutdown:
            _ = self.system_clock.get_elapsed_time_since_last_call(self.control_clock_id) # mark first call
            with self.control_lock:
                print("Running command ", self.command.get_name())
                self.command.execute(self.state)
            elapsed_time = self.system_clock.get_elapsed_time_since_last_call(self.control_clock_id) # get elapsed time
            remaining_time = CONTROL_TIME - elapsed_time
            if remaining_time > 0:
                time.sleep(remaining_time)

            external_elapsed_time = self.system_clock.get_elapsed_time_since_last_call(self.control_external_clock_id) 
            self.history['control_elapsed_time'].append(external_elapsed_time)
            

    