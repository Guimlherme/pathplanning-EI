import socket
import json
import time
from maps import get_grid_map, get_quarto_map
import sys
import select

MAX_RETRIES = 9
INITIAL_TIME = 0.3

def get_connection(host, port):
    client_socket = socket.socket()  
    t = INITIAL_TIME
    count = 1
    connected = False
    while not connected:
        print(f"Trying to connect, attempt #{count}")
        try:
            client_socket.connect((host, port))  
            connected = True
        except socket.error:
            if count == MAX_RETRIES:
                break
            print("Connection failed, retrying")
            time.sleep(t)
            if t < 2:
                t *= 2
            count += 1
    if not connected:
        raise Exception('Could not connect')
    return client_socket

def client_program(config, map):
    host = config['host']
    port = config['port']

    client_socket = get_connection(host, port)

    message = input(" -> ")

    while message.lower().strip() != 'quit':
        if len(message) == 0:
            message = input(" -> ") 
            continue
        client_socket.send(message.encode()) 
        data = client_socket.recv(1024).decode()
        if message == 'u':
            print("Press enter to stop updating map")
            user_input = None
            while True:
                input_ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                for sender in input_ready:
                    if sender == sys.stdin:
                        user_input = input()
                if user_input is None:
                    stringlist = list(data.split(" "))
                    floatlist = [float(x) for x in stringlist]
                    map.print_with_robot(floatlist)
                else:
                    # user input done
                    break
                time.sleep(0.1) # map/input update time
                client_socket.send(message.encode())
                data = client_socket.recv(1024).decode()
        else:
            print('Robot response: ' + str(data))
        message = input(" -> ") 

    client_socket.close() 


if __name__ == '__main__':
    with open("config.json", "r") as f:
        config = json.load(f)
    map = get_grid_map(client=True)
    client_program(config, map)
