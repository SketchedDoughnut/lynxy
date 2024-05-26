# this below code has been contributed to by chat gpt
import socket
import time

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

# define all global vars
HOST, PORT = '', valid_ports[0] # localhost
main_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# override info
_ov_ports = []
_do_print = True





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





## FUNCTIONS - operations
# cycles port connection
def _cycle_port(client: socket.socket) -> socket.socket:
    '''
    An internal function used to cycle through the ports in valid_ports to try and find a connection
    '''
    connected = False
    for port in valid_ports:
        try:
            pprint(f'[PORT CYCLE] Client trying port: {port}')
            client.connect((HOST, port))
            pprint(f'[PORT CYCLE] Client connected to: {port}')
            pprint('----------------------------------------------')
            connected = True
            break
        except IndexError:
            port = valid_ports[0]
            pprint(f'[PORT CYCLE - RESET 1] Client resetting port to: {port}')
        except:
            try:
                pprint(f'[PORT CYCLE] Client port cycling: {port} -> {valid_ports[valid_ports.index(port) + 1]}')
            except IndexError:
                port = valid_ports[0]
                pprint(f'[PORT CYCLE - RESET 2] Client resetting port to: {port}')
    if connected == True:
        return client, port
    else:
        pprint('[PORT CYCLE] the client can not find a open valid server port, exiting')
        exit()



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
def submit_username_data(message: str) -> None:
    '''
    Submits a username to the server, which the server will associate with your IP and port
    '''
    # local override for package form
    client = main_client
    encoded_message = message.encode('utf-8')
    client.sendall(encoded_message)
    pprint(f"Sent:     {message}")
    incoming_data = client.recv(1024).decode('utf-8')
    pprint(f"Received: {incoming_data}")

# requests ip and port from server
def request_username_data(message: str) -> None:
    '''
    requests data associated with a username from the server
    '''
    # local override for package form
    client = main_client
    encoded_message = message.encode('utf-8')
    client.sendall(encoded_message)
    pprint(f"Sent:     {message}")
    # incoming_data = full_recieve(client)
    incoming_data = client.recv(1024).decode('utf-8')
    pprint(f"Received: {incoming_data}")

# a general message sender
def general_send(message: str) -> None:
    '''
    A general tool function for sending messages to the recipient (server, other client, etc)
    '''
    # local override for package form
    client = main_client
    encoded_message = message.encode('utf-8')
    client.sendall(encoded_message)
    pprint(f"Sent:     {message}")
    # incoming_data = full_recieve(client)
    incoming_data = client.recv(1024).decode('utf-8')
    pprint(f"Received: {incoming_data}")



def start_client(connection_ip: str) -> None:
    '''
    Starts the connection to the server, taking in an IP
    '''
    global main_client, valid_ports, PORT, HOST
    HOST = connection_ip

    # overrides
    if len(_ov_ports) > 0:
        valid_ports = _ov_ports
        PORT = valid_ports[0]
        pprint(f'[OVERRIDE] Overrided ports to: {valid_ports}')
    
    # establish the connection to a port that the server is on
    main_client, PORT = _cycle_port(main_client)