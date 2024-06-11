import socket
# import time
import pickle
import threading

# installs
import rsa

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

# define all global vars
_HOST, _PORT = '', _valid_ports[0] # local_HOST
_main_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# override info
_ov_ports = []
_do_print = False

# status vars
_connected = False

# safety vars
_server_public_key = 0
_client_private_key = 0
_client_public_key = 0

# listener features
message_queue = []

## FUNCTIONS - overrides, features
def override_ports(ports: list) -> None:
    ''' 
    Overrides what ports the client will attempt to connect to
    '''
    global _ov_ports
    _ov_ports = ports

# disable prints
def disable_print() -> None:
    '''
    Disables the client from printing messages
    '''
    global _do_print
    _do_print = False

# enable prints
def enable_print() -> None:
    '''
    Enables the client to print messages
    '''
    global _do_print
    _do_print = True

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
    Returns data about the current client in the form of a dictionary
    '''
    return {
        'client info': {
            'ip': _HOST,
            'port': _PORT
        },
        'data': {
            'message_queue': message_queue
        },
        'sillies': 'sillies :3'
    }


























## FUNCTIONS - safety
def _gen_access_keys() -> tuple:
    '''
    Generates a public and private key, and returns them in a tuple
    '''
    public_key, private_key = rsa.newkeys(1024)
    return public_key, private_key

def _handshake(client: socket.socket) -> None:
    global _client_private_key, _client_public_key, _server_public_key

    pprint('[CLIENT HANDSHAKE] Handshaking with server...')
    # generate public and private keys (OBJECTS)
    _client_public_key, _client_private_key = _gen_access_keys()
    # pprint('[HANDSHAKE]: generating public and private key')

    # get servers public key (BYTES -> OBJECT)
    pickled_server_public_key = client.recv(1024)
    _server_public_key = pickle.loads(pickled_server_public_key)
    # pprint('[HANDSHAKE]: getting server public key')

    # pickle and send our public key (OBJECT -> BYTES)
    pickled_client_public_key = pickle.dumps(_client_public_key)
    client.sendall(pickled_client_public_key)
    # pprint('[HANDSHAKE]: sending public key')

    # print('client priv key:', _client_private_key)
    # print('client pub key:', _client_public_key)
    # print('client server pub key:', _server_public_key)

def _encrypt_public(data) -> bytes:
    pickled_data = pickle.dumps(data)
    encoded_data = rsa.encrypt(pickled_data, _server_public_key)
    return encoded_data

def _decrypt_private(data) -> any:
    decrypted_data = rsa.decrypt(data, _client_private_key)
    loaded_data = pickle.loads(decrypted_data)
    return loaded_data



















## FUNCTIONS - operations
# cycles port connection
def _cycle_port(client: socket.socket) -> tuple[socket.socket, int, bool]:
    global _connected
    '''
    An internal function used to cycle through the ports in _valid_ports to try and find a connection
    '''
    _connected = False
    out_port = 0
    for port in _valid_ports:
        out_port = port
        try:
            pprint(f'[PORT CYCLE] Client trying port: {port}')
            client.connect((_HOST, port))
            pprint(f'[PORT CYCLE] Client connected to: {port}')
            pprint('----------------------------------------------')
            _connected = True
            break
        except IndexError:
            port = _valid_ports[0]
            pprint(f'[PORT CYCLE - RESET 1] Client resetting port to: {port}')
        except:
            try:
                pprint(f'[PORT CYCLE] Client port cycling: {port} -> {_valid_ports[_valid_ports.index(port) + 1]}')
            except IndexError:
                port = _valid_ports[0]
                pprint(f'[PORT CYCLE - RESET 2] Client resetting port to: {port}')
    if _connected == True:
        _handshake(client)
        return client, out_port, True
    elif _connected == False:
        pprint('[PORT CYCLE] the client can not find a open valid server port, exiting')
        return client, _PORT, False




































# a function to fully recieve the message from server (to try and prevent loss)
# def full_recieve(client: socket.socket) -> str:
#     message_length = len(client.recv(1024).decode('utf-8'))
#     incoming_message = ''
#     local_length = 0
#     while local_length <= message_length:
#         incoming_message += client.recv(1024).decode('utf-8')
#         local_length = len(incoming_message)
#     return incoming_message

# a function for submitting username data to the server
def submit_username_data(username: str) -> str:
    '''
    Submits a username to the server, which the server will associate with your IP and port.
    Returns a message that confirms that the action has happened.
    '''
    # local override for package form
    client = _main_client
    message = username
    # encoded_message = message.encode('utf-8')
    message2 = f'username {message}'
    # encoded_message = message2.encode('utf-8') # added username prefix by default
    encoded_message = _encrypt_public(message2)
    client.sendall(encoded_message)
    pprint(f"Sent:     {message2}")
    # incoming_data = client.recv(1024).decode()\
    incoming_data = client.recv(1024)
    incoming_data = _decrypt_private(incoming_data)
    pprint(f"Received: {incoming_data}")
    return incoming_data

# requests ip and port from server
def request_username_data(username: str) -> any:
    '''
    requests data associated with a username from the server, and either returns a status code, meaning you entered an invalid username, 
    or returns the IP and port of the user in a list.
    '''
    # local override for package form
    client = _main_client
    message = username
    # encoded_message = message.encode('utf-8')
    message2 = f'request_by_user {message}'
    # encoded_message = message2.encode('utf-8') # added request_by_user prefix by default
    encoded_message = _encrypt_public(message2)
    client.sendall(encoded_message)
    pprint(f"Sent:     {message2}")
    # incoming_data = full_recieve(client)
    # incoming_data = client.recv(1024).decode('utf-8')
    incoming_data = client.recv(1024)
    incoming_data = _decrypt_private(incoming_data)
    pprint(f"Received: {incoming_data}")
    if incoming_data == '100':
        return incoming_data

    # parse into list
    # address_str = incoming_data.strip('()')
    # ip_str, port_str = address_str.split(',')
    # ip_str = ip_str.strip().strip("'")
    # port_int = int(port_str.strip())
    # incoming_data = [ip_str, port_int]
    return incoming_data

# a general message sender
def send_msg(data: any, recieve: bool = True) -> any:
    '''
    A general tool function for sending messages to the recipient (server, other client, etc)
    '''
    message = data
    # local override for package form
    client = _main_client
    # encoded_message = message.encode('utf-8')
    encoded_message = _encrypt_public(message)
    # print('CLIENT: ENCRYPTED:', encoded_message)
    client.sendall(encoded_message)
    pprint(f"Sent:     {message}")
    # incoming_data = full_recieve(client)
    if recieve:
        # incoming_data = client.recv(1024).decode('utf-8')
        incoming_data = client.recv(1024)
        incoming_data = _decrypt_private(incoming_data)
        pprint(f"Received: {incoming_data}")
        return incoming_data

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



# function for shutting down the client
def shutdown_client() -> bool:
    '''
    A function to shut down the client: returns a bool telling you whether it worked or not.
    '''
    global _main_client
    try:
        send_msg('end_session')
    except:
        pass
    try:
        _main_client.close()
        pprint('[CLIENT SHUTDOWN] Shutting down client...')
        return True
    except:
        return False

def start_client(connection_ip: str) -> bool:
    '''
    Starts the connection to the server, taking in an IP. 
    This function returns a bool, telling you whether it worked or not.
    '''
    global _main_client, _valid_ports, _PORT, _HOST
    _HOST = connection_ip

    # reset _main_client
    _main_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # overrides
    if len(_ov_ports) > 0:
        _valid_ports = _ov_ports
        _PORT = _valid_ports[0]
        pprint(f'[OVERRIDE] Overrided ports to: {_valid_ports}')
    
    # establish the connection to a port that the server is on
    _main_client, _PORT, state = _cycle_port(_main_client)
    return state


def start_client_listener() -> None:
    '''
    A function that acts on the recieving end to recieve information from the server. It adds to a message queue that can be accessed to retrieve data. 
    The latest entry in the data queue is the newest information. The queue gets cleared after 25 entries for efficiency and optimal storage.
    '''
    send_msg('listener')
    threading.Thread(target=lambda:_internal_client_listener()).start() # actual listener
    threading.Thread(target=lambda:_inbound_data_parser()).start() # parser to get individual commands
    threading.Thread(target=lambda:_parsed_data_decrypter()).start() # decrypts each command, goes into message queue
    # threading.Thread(target=lambda:_message_queue_cleaner()).start() # cleaner for list, saves latest val

def _message_queue_cleaner():
    global message_queue
    while True:
        if len(message_queue) > 25: # currently hard set value
            try:
                latest = message_queue[-1]
                # latest = message_queue[-5:]
                # print('saving latest:', latest)
                message_queue = [latest]
                # message_queue = latest
                # print('set new message queue to:', message_queue)
                # message_queue = []
                # print('cleaning data queue')
            except Exception as e:
                # print('clean error:', e)
                pass

#######################################################################################

_inbound_data = []
_parsed_data = [] 
# this function is responsible for decrypting and finally outputting data to the message queue
def _parsed_data_decrypter():
    while True:
        for parsed in _parsed_data:
            # print('[DECRYPTER] Decrypting:', parsed)
            try:
                decoded = _decrypt_private(parsed)
                # print('NEW DECRYPTED:', decoded)
                message_queue.append(decoded)
            except Exception as e:
                print('NEW DECRYPTION LOST:', e)
                # packet loss
                pass
            _parsed_data.remove(parsed)
            # exit()

# this function creates a parser which isolates each message
def _inbound_data_parser():
    while True:
        for data in _inbound_data:
            decoded_data = data.decode()
            # print('[PARSER] Parsing:', decoded_data)
            split_entry = [str(i) for i in decoded_data]
            new_segment = ''
            for letter in split_entry:
                if letter == '~':
                    location = split_entry.index(letter)
                    try:
                        next = split_entry[location + 1]
                        if next == 'E':
                            # new_segment = new_segment.encode()
                            new_segment = eval(new_segment)
                            # print('NEWS SEGMENT:', new_segment)
                            _parsed_data.append(new_segment)
                            new_segment = ''
                            break
                    except Exception as e:
                        print('NEW SEGMENT LOST:', e)
                        # cant go farther, lost packet
                        pass
                else:
                    new_segment += letter
            _inbound_data.remove(data)
            # exit()

# this function is responsible for taking in messages
def _internal_client_listener():
    global message_queue
    while True:
        ## OLD CODE
        # data = _main_client.recv(1024)
        # try:
        #     decoded = _decrypt_private(data)
        # except Exception as e:
        #     # print('packet loss error:', e)
        #     continue # packet loss
        # if decoded == '000':
        #     continue
        # # print('adding message to queue:', len(message_queue) + 1)
        # # print('recieved packet:', decoded)
        # message_queue.append(decoded)
        # # print('message queue:', message_queue)

        ## NEW CODE
        data = _main_client.recv(1024)
        _inbound_data.append(data)
        # print('[LISTENER] Recieving:', data)
        # exit()