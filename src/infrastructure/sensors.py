from .robust_serial import write_order, Order, write_i8, write_i16, read_i16, read_i32, read_i8
from .robust_serial.utils import open_serial_port
import struct

import perception
import numpy as np 

class ArduinoSensors:
    def __init__(self, arduino, debug=False):
        self.debug = debug
        self.arduino = arduino

    def camera_shot(self):# TODO get from the camera
        image = np.zeros((64, 64, 3), np.uint8)
        image[:, 30:32, :] = 1
        return image

    def left_encoder(self):
        write_order(self.arduino.serial_file, Order.READENCODERl)
        while True:
            try:
                g = read_i16(self.arduino.serial_file)
                break
            except struct.error:
                pass
            except TimeoutError:
                write_order(self.arduino.serial_file, Order.READENCODERl)
                pass
        return g

    def right_encoder(self):
        write_order(self.arduino.serial_file, Order.READENCODERr)
        while True:
            try:
                d = read_i16(self.arduino.serial_file)
                break
            except struct.error:
                pass
            except TimeoutError:
                write_order(self.arduino.serial_file, Order.READENCODERr)
                pass
        return d

    def ultrassound_distance(self):
        # TODO get correct value
        return 0.4
