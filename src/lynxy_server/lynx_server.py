import socketserver
import socket

# where client data is stored
client_dict = {
    'default': 0
}

# all valid ports it will attempt to connect to
valid_ports = [
    11111,
    12111,
    11211,
    11121,
    11112,
    22111,
    12211,
    11221,
    11122,
    22222
]

# host and port info for connections
HOST = socket.gethostbyname(socket.gethostname())
PORT = valid_ports[0]

# override info
ov_ip = ''
do_print = True



## OVERRIDE FUNCTIONS
# override ports
def override_ports(ports: list) -> None:
    global valid_ports, PORT
    valid_ports = ports
    PORT = valid_ports[0]

# override ip
def ovveride_ip(ip_in: str) -> None:
    global ov_ip
    ov_ip = ip_in

# disable prints
def disable_print() -> None:
    global do_print
    do_print = False

# enable prints
def enable_print() -> None:
    global do_print
    do_print = True



# function to handle printing
def pprint(msg: str) -> None:
    if do_print:
        print(msg)
    else:
        pass



# MAIN CLASS
class myTCPserver(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        global client_dict
        while True:
            # format incoming message
            msg = bytes(self.request.recv(1024)).decode('utf-8')
            split_msg = msg.split()
            prefix = split_msg[0]
            split_msg.remove(prefix)
            joined_msg = "".join(split_msg)

            # if prefix is username, log their username and their device info (ip, port) associated with it
            if prefix == 'username':
                client_dict[joined_msg] = self.client_address
                pprint(f'[{self.client_address[0]}] {prefix} - logging {self.client_address} to {joined_msg}')
                self.request.sendall('logged username, data'.encode('utf-8'))

            # if prefix is request_by_user, attempt to return the data associated with that username. If it does not exist, send back "None"
            elif prefix == 'request_by_user':
                try:
                    self.request.sendall(str(client_dict[joined_msg]).encode('utf-8'))
                    pprint(f'[{self.client_address[0]}] {prefix} - return {joined_msg} data: {client_dict[joined_msg]}')
                except:
                    self.request.sendall('None'.encode('utf-8'))

            # if msg is end_session, end the current session the server and the client have
            elif msg == 'end_session':
                self.request.sendall('ending'.encode('utf-8'))
                pprint(f'[{self.client_address[0]}] {msg} - ending this instance')
                pprint('----------------------------------------------')
                break
            
            # ignore their message if otherwise
            else:
                # self.request.sendall(msg.upper().encode('utf-8'))  # Send response back to the client
                pass



# main function for starting
def start_server() -> None:
    global HOST, PORT
    ## apply overrides
    # override ip
    if ov_ip:
        HOST = ov_ip

    # pre-loop variables
    connected = False
    
    # loop, trying to find a free port
    for port in valid_ports:

        try:
            pprint(f'[PORT CYCLE] Server trying port: {port}')
            with socketserver.ThreadingTCPServer((HOST, port), myTCPserver) as server:
                pprint(f'[PORT CYCLE] Server found port for startup: {port}')
                pprint('----------------------------------------------')
                connected = True
                PORT = port
                server.serve_forever()
                break
        # except IndexError:
        #     port = valid_ports[0]
        #     print(f'[PORT CYCLE - RESET 1] Server resetting port to: {port}')
        except:
            try:
                pprint(f'[PORT CYCLE] Server port cycling: {port} -> {valid_ports[valid_ports.index(port) + 1]}')
            except IndexError:
                port = valid_ports[0]
                pprint(f'[PORT CYCLE - RESET 2] Server resetting port to: {port}')
    
    if connected == False:
        pprint('Server failed to find an open valid port, exiting')
        exit()