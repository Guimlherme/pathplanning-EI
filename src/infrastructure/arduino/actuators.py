from .robust_serial import write_order, Order, write_i8, write_i16, read_i16, read_i32, read_i8
from time import sleep
from command import Actuator

motor_speed=100

class ArduinoActuators(Actuator):
    def __init__(self, arduino):
        self.arduino = arduino

    def set_speeds(self, right, left):
        write_order(self.arduino.serial_file, Order.MOTOR)
        write_i8(self.arduino.serial_file, right*motor_speed) #valeur moteur droit
        write_i8(self.arduino.serial_file, left*motor_speed) #valeur moteur gauche