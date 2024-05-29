import socketserver
import socket
import threading
import time
import random

# file imports
from .responses import *
from .toggles import *

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
_shutdown = False
_kill_all = False

# server obj for shutting down
_server = 0

# starting thread object
_starting_thread = 0

# server token
_token = 'x'
_verified = False







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
        'server info': {
            'is_alive': _connected,
            'ip': _HOST,
            'port': _PORT,
            'token': _token
        },
        'client info': _client_dict
    }

# function for shutting down the server
def freeze_server(do_print: bool = True) -> str:
    '''
    A function to shut down the server: returns a status code.
    '''
    global _server, _kill_all
    try:
        _server.shutdown()
        _kill_all = True
        if do_print == True:
            pprint('[SERVER SHUTDOWN] Shutting down server...')
        return OPERATION_SUCCESS.decode()
    except:
        return OPERATION_FAIL.decode()
    
# function to poll shutdown var, if it is enabled then shutdown
def _poll_shutdown() -> None:
    global _kill_all
    while True:
        if _shutdown == True:
            pprint('[SERVER SHUTDOWN] request to shutdown detected, shutting down server...')
            freeze_server(False)
            pprint('[SERVER SHUTDOWN] Enabling _kill_all...')
            _kill_all = True
            pprint('[SERVER SHUTDOWN] Server shut down, exiting...')
            break
        time.sleep(5)
    exit()

## SAFETY FUNCTIONS
# function to generate an auth token that someone can use to remotely control the server
def _gen_auth_token() -> str:
    '''
    A function that generates an auth token for the user to use to remotely connect and control the server
    '''
    lower_alpha = 'abcdefghijklmnopqrstuvwxyz'
    upper_alpha = lower_alpha.upper()
    letter_list = [lower_alpha, upper_alpha]
    token = ''
    for i in range(6): # length of your sign-in token
        letter_or_num = random.randint(0, 1)
        if letter_or_num == 0:
            letter_type = random.randint(0, 1)
            letter_range = letter_list[letter_type]
            letter_index = random.randint(0, len(letter_range) - 1)
            token += letter_range[letter_index]
        elif letter_or_num == 1:
            token += str(random.randint(0, 9))
    return token


# MAIN CLASS
class _myTCPserver(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        global _client_dict, _verified, _shutdown

        saved_username = ''
        while True:
            # establish client address
            addr = self.client_address[0]
            addr = self.client_address[1]

            # kill client communication if is true (will kill before msg)
            if _kill_all == True:
                # self.request.sendall('the server has been commanded to kill all client instances'.encode())
                self.request.sendall(KILL_ALL)
                pprint(f'[{addr}] Killing this instance, due to _kill_all being True...')
                break

            # format incoming message
            try:
                msg = bytes(self.request.recv(1024)).decode('utf-8')
                split_msg = msg.split()
                prefix = split_msg[0]
                split_msg.remove(prefix)
                joined_msg = "".join(split_msg)
            except:
                try:
                    self.request.sendall(INVALID_MESSAGE) # try to send message telling them what they gave is invalid
                    continue
                except Exception as e:
                    pprint(f'[{addr}] - crash - ending this instance')
                    pprint('----------------------------------------------')
                    break

            # if prefix is username, log their username and their device info (ip, port) associated with it
            if prefix == 'username':
                if joined_msg: # if not empty

                    # if they have not already inputted a username and the username limit is not on,
                    if limit_username == True: # if username limit is enabled
                        if saved_username: # if they have already submtited a username,
                            self.request.sendall(ALREADY_REGISTERED_USERNAME) # tell them they have already registered a username
                            continue # start next loop iteration
                        else: # else, they have not submitted a username
                            if overwrite_usernames == True: # if they want to overwrite usernames
                                pprint(f'[{addr}] {prefix} - logging {self.client_address} to {joined_msg}')
                                _client_dict[joined_msg] = self.client_address # write username regardless
                                self.request.sendall(OPERATION_SUCCESS) # send back success
                                continue # start next loop iteration
                            else: # if they do not want to overwrite usernames
                                try: # see if the entry exists
                                    _client_dict[joined_msg] # try to access entry
                                    self.request.sendall(USERNAME_EXISTS) # if entry exists, no error, returns exists
                                    continue # start next loop iteration
                                except KeyError: # fails since no key exists
                                    _client_dict[joined_msg] = self.client_address # set username since it does not exist
                                    pprint(f'[{addr}] {prefix} - logging {self.client_address} to {joined_msg}')
                                    saved_username = joined_msg
                                    self.request.sendall(OPERATION_SUCCESS)
                    else:
                        if overwrite_usernames == True:
                            pprint(f'[{addr}] {prefix} - logging {self.client_address} to {joined_msg}')
                            _client_dict[joined_msg] = self.client_address # write username regardless
                            self.request.sendall(OPERATION_SUCCESS) # send back success
                            continue # start next loop iteration
                        else:
                            try: # see if the entry exists
                                _client_dict[joined_msg] # try to access entry
                                self.request.sendall(USERNAME_EXISTS) # if entry exists, no error, returns exists
                                continue # start next loop iteration
                            except KeyError: # fails since no key exists
                                _client_dict[joined_msg] = self.client_address # set username since it does not exist
                                pprint(f'[{addr}] {prefix} - logging {self.client_address} to {joined_msg}')
                                saved_username = joined_msg
                                self.request.sendall(OPERATION_SUCCESS)

                        # pprint(f'[{addr}] {prefix} - logging {self.client_address} to {joined_msg}')
                        # # self.request.sendall('logged username, data'.encode())
                        # self.request.sendall(OPERATION_SUCCESS)
                else:
                    self.request.sendall(INVALID_MESSAGE)

            # if prefix is request_by_user, attempt to return the data associated with that username. If it does not exist, send back "None"
            elif prefix == 'request_by_user':
                try:
                    self.request.sendall(str(_client_dict[joined_msg]).encode())
                    pprint(f'[{addr}] {prefix} - return {joined_msg} data: {_client_dict[joined_msg]}')
                except:
                    pprint(f'[{addr}] {prefix} - return {joined_msg} data: None')
                    # self.request.sendall('None'.encode())
                    self.request.sendall(INVALID_USERNAME_DATA)

            # if prefix is auth, check if token is matching, then allow user to use dev features
            elif prefix == 'auth':
                if joined_msg == _token:
                    _verified = True
                    # self.request.sendall('client session authorized'.encode())
                    self.request.sendall(OPERATION_SUCCESS)
                    pprint(f'[{addr}] {prefix} - authed client')
                else:
                    # self.request.sendall('invalid auth token'.encode())
                    self.request.sendall(INVALID_AUTH_TOKEN)

            # if msg is clear_client, check if this client is authorized and then clear the client_dict
            elif msg == 'clear_client':
                if _verified == True:
                    _client_dict = {
                        'default': 0
                    }
                    # self.request.sendall('cleared client dictionary')
                    self.request.sendall(OPERATION_SUCCESS)
                    pprint(f'[{addr}] {msg} - clearing client_dict')
                else:
                    # self.request.sendall('user not authorized'.encode())
                    self.request.sendall(USER_NOT_AUTHORIZED)


            # if msg is freeze_server, check if this client is authorized and then raise the flag to shutdown srever
            elif msg == 'freeze_server':
                if _verified == True:
                    _shutdown = True
                    # self.request.sendall('shutdown of server requested, raising flag'.encode())
                    self.request.sendall(OPERATION_SUCCESS)
                    pprint(f'[{addr}] {msg} - shutdown of server requested, raising flag')
                else:
                    # self.request.sendall('user not authorized'.encode())
                    self.request.sendall(USER_NOT_AUTHORIZED)

            # if msg is end_session, end the current session the server and the client have
            elif msg == 'end_session':
                # self.request.sendall('ending'.encode())
                self.request.sendall(END_SESSION)
                pprint(f'[{addr}] {msg} - ending this instance')
                pprint('----------------------------------------------')
                break
            
            # ignore their message if otherwise
            else:
                # self.request.sendall(msg.upper().encode())  # Send response back to the client
                # self.request.sendall('invalid command'.encode())
                self.request.sendall(INVALID_COMMAND)
                pass


# main function for starting, does not use a thread and will block code
def no_thread_start_server(is_threaded: bool = False) -> None:
    '''
    If you want to start the server without it running in a thread, you can call this function. However, this will block your code until the server goes offline.
    This won't happen unless it crashes, or you remotely raise the shutdown flag (refer to the server setup page of documentation on Github)
    '''
    global _HOST, _PORT, _valid_ports, _connected, _server, _token
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
    _connected = False
    
    # generate unique session token for remote controlling the server
    _token = _gen_auth_token()

    # loop, trying to find a free port
    for port in _valid_ports:

        try:
            pprint(f'[PORT CYCLE] Server trying port: {port}')
            with socketserver.ThreadingTCPServer((_HOST, port), _myTCPserver) as _server:
                pprint(f'[PORT CYCLE] Server found port for startup: {port}')
                # start server shutdown poll
                threading.Thread(target=lambda:_poll_shutdown()).start()    # , daemon=True).start()
                pprint('[SERVER] Started scan for shutdown requests')
                if is_threaded: 
                    pprint(f'[SERVER] Server IP: {_HOST}')
                    pprint(f'[SERVER] Control token: {_token}')
                else: 
                    print(f'[SERVER] Server IP: {_HOST}')
                    print(f'[SERVER] Session token: {_token}')
                pprint('[SERVER] Server is ready for communication~!')
                if is_threaded:
                    pprint('----------------------------------------------')
                else: 
                    print('----------------------------------------------')
                _connected = True
                _PORT = port
                _server.serve_forever()
                break
        except:
            try:
                pprint(f'[PORT CYCLE] Server port cycling: {port} -> {_valid_ports[_valid_ports.index(port) + 1]}')
            except IndexError:
                port = _valid_ports[0]
                pprint(f'[PORT CYCLE - RESET 2] Server resetting port to: {port}')
    
    if _connected == False:
        pprint('[PORT CYCLE - ERROR 0] Server failed to find an open valid port, exiting')
        exit()
    else:
        pprint('[PORT CYCLE - ERROR 1] It is assumed server has been shutdown, ignoring error')





# starts the server via a thread, to let the code calling this function continue running instead of blocking
def start_server() -> tuple:
    global _starting_thread
    '''
    Starts the server in a thread, which means this will not block the rest of your code if you have more things done after this function is called. 
    This function also returns the IP that the server is on, the port the server is on, and the authorization token in a tuple.
    '''
    _starting_thread = threading.Thread(target=lambda:no_thread_start_server(True)) #, daemon=True)
    _starting_thread.start()
    time.sleep(0.25) # this is to not get false information if they request data later on 
    return _HOST, _PORT, _token