import socket
import json

def client_program(config):
    host = config['host']
    port = config['port']

    client_socket = socket.socket()  
    client_socket.connect((host, port))  

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