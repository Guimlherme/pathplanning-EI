import socket
import signal

class Network:
    def __init__(self, control_panel, config):
        self.control_panel = control_panel
        self.config = config
        self.start_server()
        self.shutdown = False
        self.position = [0, 0, 0]

    def start_server(self):
        host = self.config.get_setting('host')
        port = self.config.get_setting('port')

        self.server_socket = socket.socket() 
        try:
            self.server_socket.bind((host, port))
        except:
            raise Exception("Could not start server")

    def read(self): 
        # configure how many client the server can listen simultaneously
        self.server_socket.listen(1)
        try:
            conn, address = self.server_socket.accept() 
        except:
            print("Exiting network, no connection established")
            return
        print("Connection from: " + str(address))
        while not self.shutdown:
            data = conn.recv(1024).decode()
            if not data:
                break # if data is not received break
            if str(data) != 'u':
                print("Received from network: " + str(data))
            result = self.parse(data)
            conn.send(result.encode()) 
        conn.close() 

    def close(self):
        self.server_socket.shutdown(socket.SHUT_RDWR)
    
    def parse(self, data):
        commands = data.split(' ')
        if commands[0] == 'r':
            self.control_panel.run = True
        elif commands[0] == 's':
            self.control_panel.run = False
        elif commands[0] == 't':
            try:
                vx = int(commands[1])
                vy = int(commands[2])
            except ValueError as ve:
                return "Bad format: must be integers"
            self.control_panel.set_target(vx, vy)
        elif commands[0] == 'i':
            try:
                x = int(commands[1])
                y = int(commands[2])
                theta = float(commands[3])
            except ValueError as ve:
                return "Bad format"
            self.control_panel.reset_state(x, y, theta)
        elif commands[0] == 'u':
            return str(self.position[0])+" "+str(self.position[1])+" "+str(self.position[2])
        else:
            return "Could not parse command"
        return "OK"

    def update_position_message(self, state):
        self.position = [state.x, state.y, state.theta]
