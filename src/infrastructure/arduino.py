from __future__ import division, print_function

import time
import numpy as np
from time import sleep
import struct

try:
    import queue
except ImportError:
    import Queue as queue

from robust_serial import write_order, Order, write_i8, write_i16, read_i16, read_i32, read_i8
from robust_serial.utils import open_serial_port
from constants import BAUDRATE

class Arduino:
    def __init__(self):
        self.serial_file = None
        self.left_motor_speed = 100
        self.right_motor_speed = 100
        self.step_length = 100


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


    def readLeftEncoder(self):
        write_order(serial_file, Order.READENCODERl)
        while True:
            try:
                g = read_i16(serial_file)
                break
            except struct.error:
                pass
            except TimeoutError:
                write_order(serial_file, Order.READENCODERl)
                pass
        return g

    def readRightEncoder(self):
        write_order(serial_file, Order.READENCODERr)
        while True:
            try:
                d = read_i16(serial_file)
                break
            except struct.error:
                pass
            except TimeoutError:
                write_order(serial_file, Order.READENCODERr)
                pass
        return d

    def readUltrasound(self):
        write_order(serial_file, Order.READULTRASOUND)
        while True:
            try:
                u = read_i32(serial_file)
                break
            except struct.error:
                pass
            except TimeoutError:
                write_order(serial_file, Order.READULTRASOUND)
                pass
        return u

    def resetEncoders(self):
        write_order(serial_file, Order.RESETENC)

    def setLeftMotorSpeed(self, cmd):
        self.left_motor_speed = int(cmd)
        write_order(serial_file, Order.MOTOR)
        write_i8(serial_file, self.right_motor_speed)  # valeur moteur droit
        write_i8(serial_file, self.left_motor_speed)  # valeur moteur gauche


    def setRightMotorSpeed(self, cmd):
        self.right_motor_speed = int(cmd)
        write_order(serial_file, Order.MOTOR)
        write_i8(serial_file, self.right_motor_speed)  # valeur moteur droit
        write_i8(serial_file, self.left_motor_speed)  # valeur moteur gauche

    def stopMotors(self):
        self.left_motor_speed = 0
        self.right_motor_speed = 0
        write_order(serial_file, Order.STOP)


