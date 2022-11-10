import socket
import json
import time

def get_connection(host, port):
    client_socket = socket.socket()  
    t = 0.4
    count = 1
    connected = False
    while not connected and count <= 5:
        print(f"Trying to connect, attempt #{count}")
        try:
            client_socket.connect((host, port))  
            connected = True
        except socket.error:
            print("Connection failed, retrying")
            time.sleep(t)
            count += 1
            t *= 2
    if not connected:
        raise Exception('Could not connect')
    return client_socket

def client_program(config):
    host = config['host']
    port = config['port']

    client_socket = get_connection(host, port)

    message = input(" -> ")

    while message.lower().strip() != 'quit':
        client_socket.send(message.encode()) 
        data = client_socket.recv(1024).decode()
        print('Robot response: ' + str(data)) 
        message = input(" -> ") 

    client_socket.close() 


if __name__ == '__main__':
    with open("config.json", "r") as f:
        config = json.load(f)
    client_program(config)