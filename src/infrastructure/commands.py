from .robust_serial import write_order, Order, write_i8, write_i16, read_i16, read_i32, read_i8
from .robust_serial.utils import open_serial_port
from time import sleep

motor_speed=50

class Arduino:
    def __init__(self):
        self.serial_file = None
        self.motor_speed = 100

    def connect(self):
        try:
            # Open serial port (for communication with Arduino)
            self.serial_file = open_serial_port(baudrate=BAUDRATE)
        except Exception as e:
            print('exception')
            raise e

        is_connected = False
        # Initialize communication with Arduino
        while not is_connected:
            print("Trying connection to Arduino...")
            write_order(self.serial_file, Order.HELLO)
            bytes_array = bytearray(self.serial_file.read(1))
            if not bytes_array:
                time.sleep(2)
                continue
            byte = bytes_array[0]
            if byte in [Order.HELLO.value, Order.ALREADY_CONNECTED.value]:
                is_connected = True

        time.sleep(2)
        c = 1
        while (c!=b''):
            c = self.serial_file.read(1)


class Command:
    def __init__(self, arduino):
        self.arduino = arduino

    def get_name(self):
        return "Abstract Command"

    def execute(self):
        raise Exception('Abstract Command cannot be executed')

class Stopped(Command):
    def __init__(self, arduino):
        super().__init__(arduino)

    def execute(self):
        return
    
    def get_name(self):
        return "Stopped"

class HalfTurn(Command):
    def __init__(self, angle):
        super().__init__(arduino)
        
    def execute(self):
        print("HalfTurn")

    def get_name(self):
        return "HalfTurn"

class Forward(Command):
    def __init__(self, angle):
        self.line_angle = angle
        super().__init__(arduino)

    def execute(self):
        print("Moving forward at " + str(self.arduino.motor_speed) + "%...")
        write_order(self.arduino.serial_file, Order.MOTOR)
        write_i8(self.arduino.serial_file, self.arduino.motor_speed) #valeur moteur droit
        write_i8(self.arduino.serial_file, self.arduino.motor_speed) #valeur moteur gauche
        return
    
    def get_name(self):
        return "Forward"

class ArduinoCommandFactory:
    def __init__(self, arduino):
        self.arduino = arduino

    def stopped(self):
        return Stopped(self.arduino)

    def forward(self, line_angle):
        return Forward(self.arduino, line_angle)

    def halfturn(self):
        return HalfTurn(self.arduino)
