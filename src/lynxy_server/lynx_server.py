import socketserver
import socket
import threading
import time

# where client data is stored
_client_dict = {
    'default': 0
}

# all valid ports it will attempt to connect to
_valid_ports = [
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

# _HOST and _PORT info for connections
_HOST = socket.gethostbyname(socket.gethostname())
_PORT = _valid_ports[0]

# override info
_ov_ip = ''
_ov_ports = []
_do_print = True

# status vars
_connected = False








## OVERRIDE FUNCTIONS
# override ports
def override_ports(ports: list) -> None:
    ''' 
    Overrides what ports the server will attempt to connect to
    '''
    global _valid_ports, _ov_ports
    _ov_ports = ports

# override ip
def override_ip(ip_in: str) -> None:
    '''
    Overrides what IP the server will attempt to connect to
    '''
    global _ov_ip
    _ov_ip = ip_in

# disable prints
def disable_print() -> None:
    '''
    Disables the server from printing messages
    '''
    global _do_print
    _do_print = False

# enable prints
def enable_print() -> None:
    '''
    Enables the server to print messages
    '''
    global _do_print
    _do_print = True


## FEATURE FUNCTIONS
# function to handle printing
def pprint(msg: str) -> None:
    '''
    A function meant for filtering prints based on if it is enabled or disabled - This is meant for internal use
    '''
    if _do_print:
        print(msg)
    else:
        pass

# function to display current data
def get_data() -> dict:
    '''
    Returns data about the current server in the form of a dictionary
    '''
    return {
        'is_alive': _connected,
        'ip': _HOST,
        'port': _PORT
    }





# MAIN CLASS
class __myTCPserver__(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        global _client_dict
        while True:
            # format incoming message
            msg = bytes(self.request.recv(1024)).decode('utf-8')
            split_msg = msg.split()
            prefix = split_msg[0]
            split_msg.remove(prefix)
            joined_msg = "".join(split_msg)

            # if prefix is username, log their username and their device info (ip, port) associated with it
            if prefix == 'username':
                _client_dict[joined_msg] = self.client_address
                pprint(f'[{self.client_address[0]}] {prefix} - logging {self.client_address} to {joined_msg}')
                self.request.sendall('logged username, data'.encode('utf-8'))

            # if prefix is request_by_user, attempt to return the data associated with that username. If it does not exist, send back "None"
            elif prefix == 'request_by_user':
                try:
                    self.request.sendall(str(_client_dict[joined_msg]).encode('utf-8'))
                    pprint(f'[{self.client_address[0]}] {prefix} - return {joined_msg} data: {_client_dict[joined_msg]}')
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



# main function for starting, does not use a thread and will block code
def no_thread_start_server() -> None:
    '''
    If you want to start the server without it running in a thread, you can call this function. However, this will block your code until the server goes offline.
    This won't happen unless it crashes.
    '''
    global _HOST, _PORT, _valid_ports, _connected
    ## apply overrides
    # override ip
    if _ov_ip:
        _HOST = _ov_ip
        pprint(f'[OVERRIDE] IP overrided to: {_HOST}')
    if len(_ov_ports) > 0:
        _valid_ports = _ov_ports
        _PORT = _valid_ports[0]
        pprint(f'[OVERRIDE] Valid ports overrided to: {_valid_ports}')

    # pre-loop variables
    connected = False
    
    # loop, trying to find a free port
    for port in _valid_ports:

        try:
            pprint(f'[PORT CYCLE] Server trying port: {port}')
            with socketserver.ThreadingTCPServer((_HOST, port), __myTCPserver__) as server:
                pprint(f'[PORT CYCLE] Server found port for startup: {port}')
                pprint('[SERVER] Server is ready for communication')
                pprint('----------------------------------------------')
                _connected = True
                _PORT = port
                server.serve_forever()
                break
        except:
            try:
                pprint(f'[PORT CYCLE] Server port cycling: {port} -> {_valid_ports[_valid_ports.index(port) + 1]}')
            except IndexError:
                port = _valid_ports[0]
                pprint(f'[PORT CYCLE - RESET 2] Server resetting port to: {port}')
    
    if connected == False:
        pprint('Server failed to find an open valid port, exiting')
        exit()


# starts the server via a thread, to let the code calling this function continue running instead of blocking
def start_server() -> None:
    '''
    Starts the server in a thread, which means this will not block the rest of your code if you have more things done after this function is called. 
    '''
    threading.Thread(target=lambda:no_thread_start_server(), daemon=True).start()
    time.sleep(0.25) # this is to not get false information if they request data later on 