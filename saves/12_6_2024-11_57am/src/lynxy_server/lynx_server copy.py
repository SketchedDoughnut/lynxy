################################################################## imports

# included
import socketserver
import socket
import threading
import time
import random
import pickle

# external
from cryptography.fernet import Fernet
import rsa

# file imports
# this below import is only visible because we want them to know response codes
# if they can see this, then they can see what each response code is
# hopefully leads to better understanding
# it will flood the dropdown menu of options (when they do lynxy_server.x)
from .responses import *








################################################################## variable assignment

# all valid ports it will attempt to connect to
# these ports are what the server binds to
# at least one of these ports should be the same client-side
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

# constants / toggles dictionary
# manages anything that can be changed 
LIMIT_USERNAME = 'limit usernames'
OVERWRITE_USERNAMES = 'ovewrite usernames'
CLEAR_DEAD_USERNAMES = 'clear dead usernames'
ENCRYPT_STORED_CLIENT_DATA = 'encrypt stored client data'
DEFAULT_PORTS = 'default ports'
OVERWRITE_IP = 'overwrite IP'
DO_PRINT = 'do print'
ALLOW_REMOTE_ADMIN = 'allow remote admin'
_toggles = {
    LIMIT_USERNAME: True,
    DO_PRINT: True,
    OVERWRITE_USERNAMES: False,
    CLEAR_DEAD_USERNAMES: True,
    ENCRYPT_STORED_CLIENT_DATA: True,
    ALLOW_REMOTE_ADMIN: False,
    DEFAULT_PORTS: _valid_ports,
    OVERWRITE_IP: None
}

# a dictionary / constants for flags
# these get changed depending on the states of the described things
_CONNECTED = 'connected'
_SHUTDOWN = 'shutdown'
_KILL_ALL = 'kill all'
_flags = {
    _CONNECTED: False,
    _SHUTDOWN: False,
    _KILL_ALL: False
}

# dictionary for storing client data
# this includes their port and ip, associated to their username
# this data is encrypted if _toggles[ENCRYPT_STORED_CLIENT_DATA] = True
_client_dict = {
    'default': 0
}

# where listener clients are stored
# these are clients who get game data distributed to them
_listener_list = []
_data_queue = []

# _HOST and _PORT info for connections
# This is the main connecting info for the server
_HOST = socket.gethostbyname(socket.gethostname())
_PORT = _valid_ports[0]

# server obj for shutting down
_server = 0

# starting thread object
_starting_thread = 0

# server token
# this is used to admin the current user and access the server
_token = 'x'

# main encryption tool for doing symmetrical encryption
_encryption_tool = Fernet(Fernet.generate_key())






################################################################## safety features 
# this includes stuff regarding encryption and whatnot

# generates auth token for remote control of server
def _gen_auth_token() -> str:
    '''
    This function generates an auth token that allows a client user
    access to the server, as an admin user.
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

# generates the public and private key for server
def _gen_access_keys() -> tuple:
    public_key, private_key = rsa.newkeys(1024)
    return public_key, private_key

# encrypts data for storage
def _encrypt_data(data: bytes) -> bytes:
    # returns encrypted data
    return _encryption_tool.encrypt(data)

# decrypts data from storage
def _decrypt_data(data: bytes) -> bytes:
    # returns decrypted data
    return _encryption_tool.decrypt(data)

# uses clients public key to encrypt data
def _encrypt_public(cpk, data) -> bytes:
    pickled_data = pickle.dumps(data)
    return rsa.encrypt(pickled_data, cpk)

# uses servers private key to decrypt data
def _decrypt_private(data) -> any:
    data = rsa.decrypt(data, _server_private_key)
    unpickle_data = pickle.loads(data)
    return unpickle_data

















# function data
# _do_custom_function = False
# _init_custom_function = 0
# _custom_function = 0





















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

def set_limit_username(choice: bool) -> None:
    global limit_username
    limit_username = choice

def set_overwrite_usernames(choice: bool) -> None:
    global overwrite_usernames
    overwrite_usernames = choice

def set_clear_dead_usernames(choice: bool) -> None:
    global clear_dead_usernames
    clear_dead_usernames = choice

def set_encrypt_client_data(choice: bool) -> None:
    global encrypt_client_data
    encrypt_client_data = choice

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

def _fancy_send(client: socket.socket, cpk, data) -> None:
    '''
    A function meant for fancy sending
    '''
    # print('SEND INVOKED)')
    # pickled_data = pickle.dumps(data)
    encrypted_data = _encrypt_public(cpk, data)
    client.sendall(encrypted_data)

def _fancy_recieve(client: socket.socket) -> any:
    '''
    A function meant for fancy recieving
    '''
    incoming = client.recv(1024)
    decoded = _decrypt_private(incoming)
    # print('FANCY RECIEVE: decode:', decoded)
    return decoded


def _log_user_data(key: str, data: tuple) -> None:
    global _client_dict
    if encrypt_client_data == True: # if server set to encrypt data
        # print(encrypt_client_data)
        # string_data = str(data) # convert data to string
        pickled_data = pickle.dumps(data)
        # encoded_data = string_data.encode() # encode string to bytes
        encrypted_data = _encrypt_data(pickled_data) # encrypt bytes into bytes
        data = encrypted_data
    _client_dict[key] = data # log

def _get_user_data(key: str) -> tuple:
    data = _client_dict[key] # get current data 
    if encrypt_client_data == True: # if server set to encrypt data
        decrypted_data = _decrypt_data(data) # data is already bytes, directly decrypt
        # string_data = decrypted_data.decode() # convert bytes to string
        string_data = pickle.loads(decrypted_data)
        data = string_data # set data to tuple
    return data # return for send

def _remove_dead(username: str):
    if clear_dead_usernames:
        try:
            del _client_dict[username]
        except:
            pass 

# from typing import Callable
# def load_function(loop_function: Callable) -> None:
#     global _do_custom_function, _custom_function
#     _do_custom_function = True
#     _custom_function = loop_function


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
        'client info': _client_dict,
        'listener info': _listener_list,
        'message_queue': _data_queue
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
        return OPERATION_SUCCESS
    except:
        return OPERATION_FAIL
    
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


## FUNCTIONS FOR DISTRIBUTION SERVER
def _loopback_input(client: socket.socket, cpk) -> None:
    # become brick
    time.sleep(0.025)
    while True:
        try:
            # msg = client.recv(1024).decode()
            msg = client.recv(1024)
            decoded = _decrypt_private(msg)
            # client.sendall(OPERATION_SUCCESS)
            # if isinstance(decoded, str) == True and decoded.isspace() == True:
            #     continue
            # elif not decoded:
            #     continue
            _data_queue.append([client, decoded])
            # client.sendall(OPERATION_SUCCESS)
            # _fancy_send(client, cpk, OPERATION_SUCCESS)
        except:
            # packet loss
            pass

def _distributor() -> None:
    global _data_queue
    while True:
        for message_data in _data_queue:
            ignore_client = message_data[0]
            message = message_data[1]
            for client in _listener_list:
                client_key = client[1]
                active_client = client[0]
                if active_client != ignore_client: 
                # if active_client == ignore_client: # TESTER STATEMENT
                    encoded = _encrypt_public(client_key, message)
                    try:
                        # new message segments
                        segmented = f'{encoded}~E'
                        encoded_segment = segmented.encode()
                        # active_client.sendall(encoded)
                        active_client.sendall(encoded_segment)
                    except:
                        # assume the client cant be commmunicated with, remove from ppl to send to
                        _listener_list.remove(client)
            _data_queue.remove(message_data)
            # time.sleep(0.0025) # who needs a delay anyways?

# MAIN CLASS
class _myTCPserver(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        global _client_dict, _shutdown

        is_listener = False
        _verified = False
        # local_data_queue = []
        # local_data_save = []
        saved_username = ''











        pprint('[SERVER HANDSHAKE] Handshaking with client...')
        # send public key of server to client
        pickled_server_public_key = pickle.dumps(_server_public_key)
        self.request.sendall(pickled_server_public_key)

        # recieve clients public key
        pickled_client_public_key = self.request.recv(1024)
        client_public_key = pickle.loads(pickled_client_public_key)

        # print('server priv key:', _server_private_key)
        # print('server pub key:', _server_public_key)
        # print('server client pub key:', client_public_key)















        
        while True:
            # establish client address
            addr = self.client_address[0]
            addr = self.client_address[1]

            # kill client communication if is true (will kill before msg)
            if _kill_all == True:
                # self.request.sendall('the server has been commanded to kill all client instances'.encode())
                # self.request.sendall(KILL_ALL)
                _fancy_send(self.request, client_public_key, KILL_ALL)
                pprint(f'[{addr}] Killing this instance, due to _kill_all being True...')
                _remove_dead(saved_username)
                break

            # format incoming message
            if not is_listener:
                try:
                    # msg = self.request.recv(1024)
                    # msg = msg.decode()
                    msg = _fancy_recieve(self.request)
                    if not msg:
                        _fancy_send(self.request, client_public_key, INVALID_MESSAGE)
                        continue
                    split_msg = msg.split()
                    prefix = split_msg[0]
                    split_msg.remove(prefix)
                    joined_msg = "".join(split_msg)
                except:
                    try:
                        # self.request.sendall(INVALID_MESSAGE) # try to send message telling them what they gave is invalid
                        _fancy_send(self.request, client_public_key, INVALID_MESSAGE)
                        continue
                    except Exception as e:
                        pprint(f'[{addr}] - crash - ending this instance')
                        _remove_dead(saved_username)
                        pprint('----------------------------------------------')
                        break
            
            if is_listener:
                # if len(_data_queue) > len(local_data_queue): # if there is a difference in the lists
                #     dif = len(_data_queue) - len(local_data_queue)
                #     for i in range(dif): # for amount of difference
                #         local_data_queue.append(_data_queue[-1]) # add all different objects to local data queue
                #         print('adding dif:', _data_queue[-1])
                #     print('local queue:', local_data_queue)
                #     # exit()
                #     for item in local_data_queue: # for each msg, encode 
                #         item = item.encode()
                #         for client in _listener_list: # for each client, send encoded message
                #             print('sending to client:', client)
                #             client.sendall(item)
                #         local_data_save.append(item.decode()) # save to local data save
                #         local_data_queue.pop(0) # remove most recent
                #         print('data save:', local_data_save)
                #         print('data queue:', local_data_queue)
                #     local_data_queue = []
                continue

            # if _do_custom_function:
            #     result = _custom_function(msg, self.client_address)
            #     if result == 'continue':
            #         continue
            #     elif result == 'break':
            #         _remove_dead(saved_username)
            #         break
            #     elif result == 'exit':
            #         _remove_dead(saved_username)
            #     else:
            #         pass
            # if prefix is username, log their username and their device info (ip, port) associated with it
            if prefix == 'username':
                # print('is username prfix')
                if joined_msg: # if not empty
                    # print('isnt empty')
                    # if they have not already inputted a username and the username limit is not on,
                    if limit_username == True: # if username limit is enabled
                        # print('do limit username')
                        if saved_username: # if they have already submtited a username,
                            # print('do save username')
                            # self.request.sendall(ALREADY_REGISTERED_USERNAME) # tell them they have already registered a username
                            # print('already registered')
                            _fancy_send(self.request, client_public_key, ALREADY_REGISTERED_USERNAME)
                            continue # start next loop iteration
                        else: # else, they have not submitted a username
                            # print('dont save username')
                            if overwrite_usernames == True: # if they want to overwrite usernames
                                # print('overwrite usernames)')
                                pprint(f'[{addr}] {prefix} - logging {self.client_address} to {joined_msg}')
                                # _client_dict[joined_msg] = self.client_address # write username regardless
                                # _log_user_data(joined_msg, (self.client_address, self.request))
                                _log_user_data(joined_msg, self.client_address)
                                saved_username = joined_msg
                                # self.request.sendall(OPERATION_SUCCESS) # send back success
                                # print('op success')
                                _fancy_send(self.request, client_public_key, OPERATION_SUCCESS)
                                continue # start next loop iteration
                            else: # if they do not want to overwrite usernames
                                # print('dont overwrite usernames')
                                try: # see if the entry exists
                                    _client_dict[joined_msg] # try to access entry
                                    # self.request.sendall(USERNAME_EXISTS) # if entry exists, no error, returns exists
                                    # print('username exists')
                                    _fancy_send(self.request, client_public_key, USERNAME_EXISTS)
                                    continue # start next loop iteration
                                except KeyError: # fails since no key exists
                                    # _client_dict[joined_msg] = self.client_address # set username since it does not exist
                                    _log_user_data(joined_msg, self.client_address)
                                    pprint(f'[{addr}] {prefix} - logging {self.client_address} to {joined_msg}')
                                    saved_username = joined_msg
                                    # self.request.sendall(OPERATION_SUCCESS)
                                    # print('op success')
                                    _fancy_send(self.request, client_public_key, OPERATION_SUCCESS)
                    else:
                        # print('dont limit usernames')
                        if overwrite_usernames == True:
                            # print('overwrite usernames')
                            pprint(f'[{addr}] {prefix} - logging {self.client_address} to {joined_msg}')
                            # _client_dict[joined_msg] = self.client_address # write username regardless
                            _log_user_data(joined_msg, self.client_address)
                            saved_username = joined_msg
                            # self.request.sendall(OPERATION_SUCCESS) # send back success
                            # print('op success')
                            _fancy_send(self.request, client_public_key, OPERATION_SUCCESS)
                            continue # start next loop iteration
                        else:
                            # print('dont overwrite usernames')
                            try: # see if the entry exists
                                _client_dict[joined_msg] # try to access entry
                                # self.request.sendall(USERNAME_EXISTS) # if entry exists, no error, returns exists
                                _fancy_send(self.request, client_public_key, USERNAME_EXISTS)
                                continue # start next loop iteration
                            except KeyError: # fails since no key exists
                                # _client_dict[joined_msg] = self.client_address # set username since it does not exist
                                pprint(f'[{addr}] {prefix} - logging {self.client_address} to {joined_msg}')
                                _log_user_data(joined_msg, self.client_address)
                                saved_username = joined_msg
                                # self.request.sendall(OPERATION_SUCCESS)
                                # print('op success')
                                _fancy_send(self.request, client_public_key, OPERATION_SUCCESS)

                        # pprint(f'[{addr}] {prefix} - logging {self.client_address} to {joined_msg}')
                        # # self.request.sendall('logged username, data'.encode())
                        # self.request.sendall(OPERATION_SUCCESS)
                else:
                    # self.request.sendall(INVALID_MESSAGE)
                    # print('invalid message')
                    _fancy_send(self.request, client_public_key, INVALID_MESSAGE)

            # if prefix is request_by_user, attempt to return the data associated with that username. If it does not exist, send back "None"
            elif prefix == 'request_by_user':
                try:
                    # self.request.sendall(str(_client_dict[joined_msg]).encode())
                    d = _get_user_data(joined_msg)
                    # self.request.sendall(d2)
                    _fancy_send(self.request, client_public_key, d)
                    pprint(f'[{addr}] {prefix} - return {joined_msg} data: {d}')
                except:
                    pprint(f'[{addr}] {prefix} - return {joined_msg} data: None')
                    # self.request.sendall('None'.encode())
                    # self.request.sendall(INVALID_USERNAME_DATA)
                    _fancy_send(self.request, client_public_key, INVALID_USERNAME_DATA)

            # if prefix is auth, check if token is matching, then allow user to use dev features
            elif prefix == 'auth':
                if _toggles[ALLOW_REMOTE_ADMIN] == False:
                    _fancy_send(self.request, client_public_key, FEATURE_DISABLED)
                    continue
                if joined_msg == _token:
                    _verified = True
                    # self.request.sendall('client session authorized'.encode())
                    # self.request.sendall(OPERATION_SUCCESS)
                    _fancy_send(self.request, client_public_key, OPERATION_SUCCESS)
                    pprint(f'[{addr}] {prefix} - authed client')
                else:
                    # self.request.sendall('invalid auth token'.encode())
                    # self.request.sendall(INVALID_AUTH_TOKEN)
                    _fancy_send(self.request, client_public_key, INVALID_AUTH_TOKEN)

            elif msg == 'help':
                msg = 'Commands: username, request_by_user, auth, help, clear_client (auth only), freeze_server (auth only)'
                # encoded = msg.encode()
                # self.request.sendall(encoded)
                _fancy_send(self.request, client_public_key, msg)
                
            # if msg is listener, add their socket to the listening list and ignore any more messages from them
            elif msg == 'listener':
                if not is_listener:
                    _listener_list.append([self.request, client_public_key])
                    is_listener = True
                    # threading.Thread(target=lambda:_loopback_input(self.request, client_public_key)).start()
                    # self.request.sendall(OPERATION_SUCCESS)
                    # time.sleep(0.025)

                    # lets create a brick
                    _fancy_send(self.request, client_public_key, OPERATION_SUCCESS)
                    pprint(f'[{addr}] {msg} - subscribing to listener')
                    _loopback_input(self.request, client_public_key)


            # if msg is clear_client, check if this client is authorized and then clear the client_dict
            elif msg == 'clear_client':
                if _verified == True:
                    _client_dict = {
                        'default': 0
                    }
                    # self.request.sendall('cleared client dictionary')
                    # self.request.sendall(OPERATION_SUCCESS)
                    _fancy_send(self.request, client_public_key, OPERATION_SUCCESS)
                    pprint(f'[{addr}] {msg} - clearing client_dict')
                else:
                    # self.request.sendall('user not authorized'.encode())
                    # self.request.sendall(USER_NOT_AUTHORIZED)
                    _fancy_send(self.request, client_public_key, USER_NOT_AUTHORIZED)


            # if msg is freeze_server, check if this client is authorized and then raise the flag to shutdown srever
            elif msg == 'freeze_server':
                if _verified == True:
                    _shutdown = True
                    # self.request.sendall('shutdown of server requested, raising flag'.encode())
                    # self.request.sendall(OPERATION_SUCCESS)
                    _fancy_send(self.request, client_public_key, OPERATION_SUCCESS)
                    pprint(f'[{addr}] {msg} - shutdown of server requested, raising flag')
                else:
                    # self.request.sendall('user not authorized'.encode())
                    # self.request.sendall(USER_NOT_AUTHORIZED)
                    _fancy_send(self.request, client_public_key, USER_NOT_AUTHORIZED)

            # if msg is end_session, end the current session the server and the client have
            elif msg == 'end_session':
                # self.request.sendall('ending'.encode())
                # self.request.sendall(END_SESSION)
                _fancy_send(self.request, client_public_key, END_SESSION)
                pprint(f'[{addr}] {msg} - ending this instance')
                # print("CHECKING CLEAR")
                _remove_dead(saved_username)
                pprint('----------------------------------------------')
                break
            
            # ignore their message if otherwise
            else:
                # self.request.sendall(msg.upper().encode())  # Send response back to the client
                # self.request.sendall('invalid command'.encode())
                # self.request.sendall(INVALID_COMMAND)
                _fancy_send(self.request, client_public_key, INVALID_COMMAND)
                pass











# FINAL VAR DEFINITIONS

# private / public key setup
_server_public_key, _server_private_key = _gen_access_keys()








# STARTING CODE

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
                # start distributor thread
                threading.Thread(target=lambda:_distributor()).start()
                pprint('[SERVER] Started distributor thread')
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