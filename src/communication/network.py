import socket

class Network:
    def __init__(self, control_panel, config):
        self.control_panel = control_panel
        self.config = config
        self.start_server()

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
        conn, address = self.server_socket.accept() 
        print("Connection from: " + str(address))
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break # if data is not received break
            print("Received from network: " + str(data))
            result = self.parse(data)
            conn.send(result.encode()) 
        conn.close() 
    
    def parse(self, data):
        commands = data.split(' ')
        if commands[0] == 'r':
            self.control_panel.run = True
        elif commands[0] == 's':
            self.control_panel.run = False
        elif commands[0] == 't':
            self.control_panel.set_target(int(commands[1]), int(commands[2]))
        else:
            return "Could not parse command"
        return "OK"
