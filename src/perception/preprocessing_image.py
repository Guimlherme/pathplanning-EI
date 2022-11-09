from __future__ import division, print_function
import cv2

import logging
import signal
import time
import numpy as np
from time import sleep
from picamera import PiCamera
import struct

try:
    import queue
except ImportError:
    import Queue as queue

from robust_serial import write_order, Order, write_i8, write_i16, read_i16, read_i32, read_i8
from robust_serial.utils import open_serial_port
from constants import BAUDRATE

camera = PiCamera()
motor_speed = 100
step_length = 5


def main():
    global camera
    camera.start_preview()
    sleep(2)
    i = 0
    moy = 0
    while i <= 40:
        start = time.time()
        my_file = test_camera()
        #image = cv2.imread('test_photo.jpg')
        preprocessing_image(my_file, i, False)
        i += 1
        end = time.time()
        moy += end - start
    moy /= 41
    print(moy)
    camera.stop_preview()

def main2():
    connect_to_arduino()
    cmd()
    start = time.time()
    end = time.time()
    while (end - start < 3):
        end = time.time()
    motor_speed = 0
    write_order(serial_file, Order.MOTOR)
    write_i8(serial_file, motor_speed)  # valeur moteur droit
    write_i8(serial_file, motor_speed) 
    


def test_camera():
    global camera
    my_file = np.empty((1280, 1024, 3), dtype = np.uint8)
    camera.capture(my_file, 'rgb')
    # At this point my_file.flush() has been called, but the file has
    return my_file


def cmd():
    global motor_speed
    write_order(serial_file, Order.MOTOR)
    write_i8(serial_file, motor_speed)  # valeur moteur droit
    write_i8(serial_file, motor_speed)  # valeur moteur gauche


def connect_to_arduino():
    global serial_file
    try:
        # Open serial port (for communication with Arduino)
        serial_file = open_serial_port(baudrate=BAUDRATE)
    except Exception as e:
        print('exception')
        raise e

    is_connected = False
    # Initialize communication with Arduino
    while not is_connected:
        print("Trying connection to Arduino...")
        write_order(serial_file, Order.HELLO)
        bytes_array = bytearray(serial_file.read(1))
        if not bytes_array:
            time.sleep(2)
            continue
        byte = bytes_array[0]
        if byte in [Order.HELLO.value, Order.ALREADY_CONNECTED.value]:
            is_connected = True

    time.sleep(2)
    c = 1
    while (c != b''):
        c = serial_file.read(1)


def preprocessing_image(image, i, save_photos=False):

    # Reescalling
    scale_percent = 30  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    # Convert to HSV color space

    blur = cv2.blur(resized, (5, 5))
    ret, thresh1 = cv2.threshold(blur, 168, 255, cv2.THRESH_BINARY)
    hsv = cv2.cvtColor(thresh1, cv2.COLOR_RGB2HSV)

    # Define range of white color in HSV
    # hue (matiz), saturation (saturação) e value (valor)
    lower = np.array([0, 0, 164])
    upper = np.array([179, 27, 255])
    mask = cv2.inRange(hsv, lower, upper)

    # Remove noise
    kernel_erode = np.ones((5, 5), np.uint8)
    eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
    kernel_dilate = np.ones((4, 4), np.uint8)
    dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)

    # Find the different contours
    _, contours, hierarchy = cv2.findContours(
        dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort by area (keep only the biggest one)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    if len(contours) > 0:
        M = cv2.moments(contours[0])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        if save_photos:
            cv2.circle(resized, (cx, cy), 5, (255, 0, 0), -1)
            for contour in contours:
                cv2.drawContours(resized, contour, -1, (0, 255, 0), 10)
            cv2.imwrite('contours.png', resized)
            cv2.imwrite('mask' + str(i) + '.png', dilated_mask)

        theta = np.arctan((cx-(width/2))/(height-cy))
        return theta

    else:
        return 0


if __name__ == '__main__':
    main2()
