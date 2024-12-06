################################################################## imports

# included
import socket
import pickle
import threading

# external
import rsa








################################################################## variable assignment

# default ports client will try and connect to
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
DO_PRINT = 'print'
DEFAULT_PORTS = 'port_override'
_toggles = {
    DO_PRINT: False,
    DEFAULT_PORTS: _valid_ports
}

# establish the main socket variables
# such as server ip, server port, main_client communicating with server
_HOST = '' # server ip
_PORT = _valid_ports[0] # server port
# _HOST, _PORT = '', _valid_ports[0] # server ip, port ip
_main_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # main client for communication with server

# status variables
# these help know what has succeeded and whatnot
_connected = False # connected to server

# safety vars
# these are used for encryption and general safety
_server_public_key = 0
_client_private_key = 0
_client_public_key = 0

# listener features for when data is distributed to clients from the other end
# this is publicly accessible so users can get data out of it
data_queue = []








################################################################## optional functions for overriding / toggles

# override ports
# used to change the ports the client tries to connect to
# def override_ports(ports: list) -> None:
#     ''' 
#     Overrides what ports the client will attempt to connect to. \n
#     ARGS
#         - ports: list
#         Each port should be an integer, and the server and the client should have at least one port in common.
#     '''
#     # global _ov_ports
#     # _ov_ports = ports
#     global _toggles
#     _toggles[DEFAULT_PORTS] = ports

# def disable_print() -> None:
#     '''
#     Disables the client from printing messages
#     '''
#     global _do_print
#     _do_print = False

# # enable prints
# def enable_print() -> None:
#     '''
#     Enables the client to print messages
#     '''
#     global _do_print
#     _do_print = True

# toggles things that are customizable
# this includes the ports to connect to, and the option to print to console
# identified as DEFAULT_PORTS and DO_PRINT
def toggle(toggle, state) -> None:
    '''
    Edits the value associated with the input "toggle". \n
    # Parameters
    **toggle** \n
    This should be set to the constants provided by lynxy, to signify what you want to change. They are listed below!
        - DO_PRINT
            - information: 
                - this toggles whether lynxy prints message to console or not. This is disabled by default.
            - values: True, False
            - example: 
                - toggle(DO_PRINT, True)
                - toggle(DO_PRINT, False)
        - DEFAULT_PORTS
            - information:
                - this regards the ports that the client will attempt to connect to on the servers IP.
            - values: list of integer ports
            - example: 
                - toggle(DEFAULT_PORTS, [12345, 23456, 34567])
            - notes: The client and the server HAVE to have at least one port in common! This is very important, 
                     because if they do not have a common port then the two can not connect. \n
    **state** \n
    State should be the corresponding value for what you entered for toggle, meaning that if for example you do `DO_PRINT`, 
    then state should either be `True` or `False`. More specific cases for states are shown above.
    '''
    global _toggles, _valid_ports
    _toggles[toggle] = state
    _valid_ports = _toggles[DEFAULT_PORTS] # update valid ports manually (idk why?)








################################################################## other general use functions (internal)

# function to handle printing if its enabled
def pprint(msg: str) -> None:
    '''
    A function meant for filtering prints based on if it is enabled or disabled - this is meant for internal use.
    # Parameters
    **msg** \n
    the information to print
    '''
    if _toggles[DO_PRINT]:
        print(msg)








################################################################## other general use functions (external)

# function to display current data
def get_data() -> dict:
    '''
    This is the main function used for acquiring data used by lynxy. The data it returns is as follows:
    - server ip
    - server port
    - ports to connect to
    - main client socket.socket object
    - boolean representing connected or not
    - toggles, including whether to print or not and the ports to connect to
    - security data, including the clients public and private key, and the servers public key
    # Returns
    - dictionary with above data
    '''
    return {
        'server info': {
            'ip': _HOST,
            'port': _PORT
        },
        'client info': {
            'default ports': _valid_ports,
            'main client': _main_client,
            'connected': _connected,
            'toggles': _toggles
        },
        # 'data': {
        #     'data_queue': data_queue
        # },
        'security': {
            'client public key': _client_public_key,
            'client private key': _client_private_key,
            'server public key': _server_public_key
        },
        'sillies': 'sillies :3'
    }








################################################################## functions for safety / security (encryption and whatnot)

# function to generate RSA public and private keys
def _gen_access_keys() -> tuple[rsa.PublicKey, rsa.PrivateKey]:
    '''
    Generates a public and private key, and returns them in a tuple like this: [public_key, private_key]
    '''
    public_key, private_key = rsa.newkeys(1024)
    return public_key, private_key


# function to do a handshake with the server, exchanging public and private keys
def _handshake(client: socket.socket) -> None:
    '''
    Does a handshake with the server, exchanging public keys.
    # Parameters
    - client: socket.socket object
    '''
    # globals
    global _client_public_key, _client_private_key # globally edit the clients public and private key
    global _server_public_key # globally edit the servers private key
    # generate keys
    pprint('[CLIENT HANDSHAKE] Handshaking with server...')
    _client_public_key, _client_private_key = _gen_access_keys() # generate public and private keys for client
    # acquire server public key
    pickled_server_public_key = client.recv(1024) # recieve pickled (pickle module turns var into bytes (var can be string, object, whatever)) public key from server
    _server_public_key = pickle.loads(pickled_server_public_key) # converts the bytes object back into its original form
    # send public key to server
    pickled_client_public_key = pickle.dumps(_client_public_key) # convert the public_key into bytes
    client.sendall(pickled_client_public_key) # send to server


# function to encrypt data when sending to server, using the servers public key
def _encrypt_public(data) -> bytes:
    '''
    A function that encrypts data using RSA, and the servers public key.
    # Parameters
    - data: any
    # Returns
    - bytes
    '''
    pickled_data = pickle.dumps(data) # converts data into bytes
    encoded_data = rsa.encrypt(pickled_data, _server_public_key) # encrypts data with servers public key
    return encoded_data


def _decrypt_private(data) -> any:
    '''
    A function that decrypts using RSA, and the clients private key
    '''
    decrypted_data = rsa.decrypt(data, _client_private_key) # decrypts data with the clients private key
    loaded_data = pickle.loads(decrypted_data) # converts bytes into data
    return loaded_data








################################################################## functions used for connecting to server (internal)

# cycles ports until a connection to the server succeeds / fails.
def _cycle_port(client: socket.socket) -> tuple[socket.socket, int, bool]:
    '''
    An internal function used to cycle through the ports in _valid_ports to try and make a connection.
    # Parameters
    - client: socket.socket object
    # Returns
    - tuple[socket.socket object of server, the port the client connected to, a boolean on whether the connection succeeded or not]
    '''
    # globals
    global _connected # indicates if the client has connected or not
    _connected = False # by default, set to False
    for port in _valid_ports: # iterate through each port
        try: # try and connect to server with current port
            pprint(f'[PORT CYCLE] Client trying port: {port}')
            client.connect((_HOST, port)) # try to connect to server ip, and the current cycled port
            pprint(f'[PORT CYCLE] Client connected to: {port}')
            pprint('----------------------------------------------')
            _connected = True # connection succeeded, set variable
            _handshake(client) # do handshake with server to exchange public keys
            return client, port, _connected # returns the client communicating with server, the port that it is connected to, and a boolean for the connection status
        except: # connection to that port failed
            try: # print that we are trying next port
                current_port_index = _valid_ports.index(port) 
                next_port = _valid_ports[current_port_index + 1]
                pprint(f'[PORT CYCLE] Client port cycling: {port} -> {next_port}')
            except IndexError: # failed, pass since the for loop will exit after this iteration is done anyways
                pass
    if _connected == False: # verify _connected is False
        pprint('[PORT CYCLE] the client can not find a open valid server port, exiting')
        return client, _PORT, _connected # return the client, _PORT as it has not changed, and a boolean for the connection status








################################################################## functions used for connecting to server / other client (external)

def start_client(connection_ip: str) -> bool:
    '''
    Starts a connection with the other end.
    # Parameters
    **connection_ip**
    the ip of the other end to connect to as a string
    # Returns
    a boolean saying whether the connection succeeded or not
    '''
    # globals
    global _main_client # client for communicating with server
    global _valid_ports # edit the valid ports for the client to connect to
    global _HOST, _PORT # servers ip, and port
    _HOST = connection_ip # set global server ip to the inputted connection_ip
    # establish connection
    _main_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # reset the main_client socket
    _valid_ports = _toggles[DEFAULT_PORTS] # set the valid ports to the ports inside of _toggles
    _main_client, _PORT, state = _cycle_port(_main_client) # establish the connection to a port that the server is on
    return state # whether the connection succeeded or not








################################################################## functions for communicating with server / other client

# sends data to server, gets data back if recieve = True
def send_msg(data: any, recieve: bool = True) -> any:
    '''
    A general messaging function for sending data to the other end (decided by what _main_client is connected to).
    # Parameters
    **data** \n
    The information you want to send to the other end. This can be anything you want! \n
    **recieve** \n
    True by default, set this to False if you do not want send_msg() to wait for a response from the other end.
    # Returns
    data recieved from other end, if recieve = True
    '''
    encoded_data = _encrypt_public(data)
    _main_client.sendall(encoded_data)
    pprint(f"Sent:     {data}")
    if recieve:
        incoming_data = _main_client.recv(1024)
        decrypted_data = _decrypt_private(incoming_data)
        pprint(f"Received: {decrypted_data}")
        return decrypted_data


# a function for submitting username data to the server
def submit_username_data(username: str) -> str:
    '''
    Submits a username to the server, which the server will associate with your IP and port. \n
    # Parameters \n
    **username** \n
    Your username as a string (please, no spaces!) \n
    # Returns \n
    a status code as a string that gives information on what happened server-side. \n
    Please note this function is meant for use only with a lynxy_server server. Otherwise, your server must be configured 
    to handle this call.
    '''
    full_data = f'username {username}'
    encrypted_data = _encrypt_public(full_data)
    _main_client.sendall(encrypted_data)
    pprint(f"Sent:     {full_data}")
    incoming_data = _main_client.recv(1024)
    decrypted_data = _decrypt_private(incoming_data)
    pprint(f"Received: {decrypted_data}")
    return decrypted_data


# requests ip and port from server
def request_username_data(username: str) -> any:
    '''
    Requests the data associated with a username from the server. 
    # Parameters
    **username** \n
    a string of the username that you want to request the data with (Please, no spaces!) \n
    # Returns \n
    a status code as a string that gives information on what happened server-side. \n
    If the server has disabled this feature, you will instead get a status code signifying a fail. 
    This might occur if the server has disabled directly connecting to other clients. 
    If this happens, then you will have to communicate with the other clients by directing traffic through the server. \n
    Please note this function is meant for use only with a lynxy_server server. Otherwise, your server must be configured 
    to handle this call.
    '''
    full_data = f'request_by_user {username}'
    # encoded_message = message2.encode('utf-8') # added request_by_user prefix by default
    encoded_message = _encrypt_public(full_data)
    _main_client.sendall(encoded_message)
    pprint(f"Sent:     {full_data}")
    # incoming_data = full_recieve(client)
    # incoming_data = client.recv(1024).decode('utf-8')
    incoming_data = _main_client.recv(1024)
    decrypted_data = _decrypt_private(incoming_data)
    pprint(f"Received: {decrypted_data}")
    return decrypted_data

    # parse into list
    # address_str = incoming_data.strip('()')
    # ip_str, port_str = address_str.split(',')
    # ip_str = ip_str.strip().strip("'")
    # port_int = int(port_str.strip())
    # incoming_data = [ip_str, port_int]








################################################################## functions for ending connections with the other end

# function for shutting down the client
def shutdown_client() -> bool:
    '''
    A function that shuts down the clients connection with the other end.
    # Returns
    a boolean telling you whether or not the shutdown succeeded
    '''
    global _main_client
    try: send_msg('end_session')
    except: pass
    try:
        _main_client.close()
        pprint('[CLIENT SHUTDOWN] Shutting down client...')
        return True
    except: return False








################################################################## functions for starting other processes

def start_listening() -> None:
    '''
    A function that acts on the recieving end to recieve information from the other end (decided by what _main_client is connected to). 
    It adds to a data queue that can be accessed to retrieve data. The latest entry in the data queue is the newest information. 
    '''
    # "The queue gets cleared after 25 entries for efficiency and optimal storage."
    send_msg('listener')
    threading.Thread(target=lambda:_inbound_data_listener()).start() # listener which recieves data
    threading.Thread(target=lambda:_inbound_data_parser()).start() # parser which identifies individual commands
    threading.Thread(target=lambda:_parsed_data_decrypter()).start() # decrypter which decrypts individual commands, this one adds to data_queue
    # threading.Thread(target=lambda:_data_queue_cleaner()).start() # cleaner for list, saves latest val








################################################################## functions / variables that are part of the listening category

_inbound_data = []
_parsed_data = []


# this function is responsible for decrypting and finally outputting data to the message queue
def _parsed_data_decrypter():
    '''
    A function that decrypts the data put into _parsed_data_decrypter, then pipes that data into data_queue.
    '''
    global _parsed_data # so we can erase current _parsed_data after making a local copy
    while True:
        lc_parsed_data = _parsed_data # lc = local_copy
        _parsed_data = [] # reset _parsed_data as we have copied locally, there is the potential for some data loss here
        for parsed_data in lc_parsed_data:
            try:
                decoded = _decrypt_private(parsed_data)
                data_queue.append(decoded)
            except Exception as e: # this error will likely happen if the parser fails to identify and assemble a proper message
                print('NEW DECRYPTION LOST:', e)
                pass
            # we do not need to remove data as that will mess with iteration
            # and once we are done iterating this data will be erased anyways
            # lc_parsed_data.remove(parsed_data) 


# this function creates a parser which identifies the start and end of a full message, joins that, then pipes it into _parsed_data
def _inbound_data_parser():
    '''
    A function that identifies the start and end of each full data packet, pieces them together, and then pipes that into _parsed_data.
    '''
    global _inbound_data
    lc_inbound_data = _inbound_data # lc = local copy
    _inbound_data = [] # reset _inbound_data as we have copied locally, there is the potential for some data loss here
    # im not really sure what happens from here down, but i think it works so oh well- not sure how i even wrote this
    # i tried to comment as best i can
    # i also renamed some stuff
    while True:
        for data in lc_inbound_data: # iterate over each piece of packet stored
            data: bytes # type hinting
            decoded_data = data.decode() # decode data
            split_entry = [str(i) for i in decoded_data] # split it into each character
            new_packet = '' # this represents the new full packet of data
            for letter in split_entry: # iterate over each character
                if letter == '~': # first marker of the end flag
                    location = split_entry.index(letter) # second marker of end flag
                    try: # try to check next character, if fails then at end of list
                        next = split_entry[location + 1]
                        if next == 'E':
                            # new_packet = new_packet.encode()
                            new_packet = eval(new_packet) # turn back into bytes??
                            _parsed_data.append(new_packet) # pipe full packet into _parsed_data
                            new_packet = '' # reset new_packet
                            break # break out of loop, currently doesn't continue searching
                    except IndexError as e:
                        print('NEW SEGMENT LOST:', e) # lost packed because could not find second part of end marker
                else:
                    new_packet += letter # add this character to the new packet
            # we do not need to remove data as that will mess with iteration
            # and once we are done iterating this data will be erased anyways
            # lc_inbound_data.remove(data)


# this function is responsible for taking in messages and piping them into _inbound_data
def _inbound_data_listener():
    '''
    A function responsible for listening for data as soon as it gets it, and piping it into _inbound_data
    '''
    while True:
        data = _main_client.recv(1024) # reccieve data
        _inbound_data.append(data) # pipe data in

        ## OLD CODE
        # data = _main_client.recv(1024)
        # try:
        #     decoded = _decrypt_private(data)
        # except Exception as e:
        #     # print('packet loss error:', e)
        #     continue # packet loss
        # if decoded == '000':
        #     continue
        # # print('adding message to queue:', len(data_queue) + 1)
        # # print('recieved packet:', decoded)
        # data_queue.append(decoded)
        # # print('message queue:', data_queue)








####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

'''
below is random code that I am not sure what to do with, so for now they remain as comments!
'''


# a function to fully recieve the message from server (to try and prevent loss)
# def full_recieve(client: socket.socket) -> str:
#     message_length = len(client.recv(1024).decode('utf-8'))
#     incoming_message = ''
#     local_length = 0
#     while local_length <= message_length:
#         incoming_message += client.recv(1024).decode('utf-8')
#         local_length = len(incoming_message)
#     return incoming_message


# def send_file(file, recieve: bool = False) -> any:
#     '''
#     A general tool function for sending files to the recipient (server, other client, etc)
#     '''
#     client = _main_client
#     encoded_file =


# def target_client(client_ip: str, client_port: int, mode: str) -> bool:
#     '''
#     Takes in the target clients ip and port, and will attempt to connect to them. If this fails, 
#     then it is possible the other client is not available.
#     This function returns a boolean, telling you whether it worked or not.
#     '''
#     global _HOST, _PORT, _valid_ports
#     global _main_client
#     global _do_print
#     # reset main_client
#     _main_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # overwrite host
#     _HOST = client_ip
#     # overwrite valid ports list
#     override_ports([client_port])
#     # overwrite port
#     _PORT = _valid_ports[0]
#     # setup other vars
#     save = _do_print

#     for i in range(30):
#         print(f'attempt {i}')
#         disable_print()
#         _main_client, _PORT = _cycle_port(_main_client)
#         _do_print = save
#         if _connected == True:
#             return True
#         time.sleep(1)
#     return False


# def _data_queue_cleaner():
#     global data_queue
#     while True:
#         if len(data_queue) > 25: # currently hard set value
#             try:
#                 latest = data_queue[-1]
#                 # latest = data_queue[-5:]
#                 # print('saving latest:', latest)
#                 data_queue = [latest]
#                 # data_queue = latest
#                 # print('set new message queue to:', data_queue)
#                 # data_queue = []
#                 # print('cleaning data queue')
#             except Exception as e:
#                 # print('clean error:', e)
#                 pass