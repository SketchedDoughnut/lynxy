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
    11122
]

# define all global vars
HOST, PORT = '', valid_ports[0] # localhost
main_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



## FUNCTIONS
# cycles port connection
def cycle_port(client: socket.socket) -> socket.socket:
    connected = False
    for port in valid_ports:
        try:
            print(f'[PORT CYCLE] Client trying port: {port}')
            client.connect((HOST, port))
            print(f'[PORT CYCLE] Client connected to: {port}')
            print('----------------------------------------------')
            connected = True
            break
        except IndexError:
            port = valid_ports[0]
            print(f'[PORT CYCLE - RESET 1] Client resetting port to: {port}')
        except:
            try:
                print(f'[PORT CYCLE] Client port cycling: {port} -> {valid_ports[valid_ports.index(port) + 1]}')
            except IndexError:
                port = valid_ports[0]
                print(f'[PORT CYCLE - RESET 2] Client resetting port to: {port}')
    if connected == True:
        return client, port
    else:
        print('[PORT CYCLE] the client can not find a open valid server port, exiting')
        exit()



# a function to fully recieve the message from server (to try and prevent loss)
def full_recieve(client: socket.socket) -> str:
    message_length = len(client.recv(1024).decode('utf-8'))
    incoming_message = ''
    local_length = 0
    while local_length <= message_length:
        incoming_message += client.recv(1024).decode('utf-8')
        local_length = len(incoming_message)
    return incoming_message



# a function for submitting username data to the server
def submit_username_data(client: socket.socket, message: str) -> None:
    encoded_message  = message.encode('utf-8')
    client.sendall(encoded_message)
    print(f"Sent:     {message}")
    incoming_data = client.recv(1024).decode('utf-8')
    print(f"Received: {incoming_data}")


# requests ip and port from server
def request_data(client: socket.socket, message: str) -> socket.socket:
    encoded_message = message.encode('utf-8')
    client.sendall(encoded_message)
    print(f"Sent:     {message}")
    # incoming_data = full_recieve(client)
    incoming_data = client.recv(1024).decode('utf-8')
    print(f"Received: {incoming_data}")



# a general message sender
def general_send(client: socket.socket, message: str) -> None:
    encoded_message = message.encode('utf-8')
    client.sendall(encoded_message)
    print(f"Sent:     {message}")
    # incoming_data = full_recieve(client)
    incoming_data = client.recv(1024).decode('utf-8')
    print(f"Received: {incoming_data}")




# establish the connection to a port that the server is on
main_client, PORT = cycle_port(main_client)

# next, send a send a message to the server
submit_username_data(main_client, 'username SketchedDoughnut')

# necessary delay
time.sleep(1)

# next, request username data
request_data(main_client, 'request_by_user SketchedDoughnut')

# necessary delay
time.sleep(1)

# finally, end the session
general_send(main_client, 'end_session')