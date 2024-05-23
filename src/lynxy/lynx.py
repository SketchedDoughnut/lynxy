import socket
import time
import threading
import json

valid_ports = [
    11111,
    12111,
    11211,
    11121,
    11112
]

# set up server ip, port to connect to
server_ip = input('enter ip: ')
# valid_ports = v.valid_ports
not_inclusive_max_port_amount = len(valid_ports) - 1
server_port = valid_ports[0]

# start client timeout
# connection_timeout = False








# def timeout_connection(timeout_time: int = 5) -> None:
#     global connection_timeout
#     init_time = time.time()
#     while True:
#         new_time = time.time()
#         dif = new_time - init_time
#         if dif >= timeout_time:
#             connection_timeout = True
#             print('timed out')
#             exit()









# def info_connect() -> dict:
#     # attempt to connect to the data server object
#     info_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     info_client.connect((server_ip, 22222))
#     active_data = info_client.recv(1024).decode('utf-8')

#     active_data = active_data.strip('{}')
#     # Split by commas to get individual key-value pairs
#     pairs = active_data.split(',')

#     # Initialize an empty dictionary to store the parsed data
#     data_dict = {}

#     # Iterate over each pair and split by colon to get key and value
#     for pair in pairs:
#         key, value = pair.split(':')
#         # Strip spaces and convert key to integer
#         key = int(key.strip())
#         # Evaluate value and store it in the dictionary
#         value = eval(value.strip())
#         data_dict[key] = value

#     return data_dict




# connects to server
def connect_to_server(client: socket.socket):
    global server_port, connection_timeout
    '''sets up the initial connection to the server, verifies it can send data over'''
    
    # connect to server ip, server port
    print('cycling connection to server until succeed / fail...')
    attempt_count = 0
    while True:
        print(f'attempt: {attempt_count}')
        try:
            print('trying port:', server_port)
            # con_thread = threading.Thread(target=lambda:client.connect((server_ip, server_port)))
            # con_thread.start()
            # tm_thread = threading.Thread(target=lambda:timeout_connection())
            # tm_thread.start()
            # if connection_timeout == True:
            #     print('timed out - main')
            # if con_thread.is_alive() == False:
            #client.connect((server_ip, server_port))
            client.connect(('localhost', server_port))
            break
        except Exception as e:
            # print('error:', e)
            # exit()
            attempt_count += 1
            if attempt_count > 0:
                print('failed, moving to next port')
                if valid_ports.index(server_port) < not_inclusive_max_port_amount:
                    server_port = valid_ports[valid_ports.index(server_port) + 1]
                    print('swapped to port', server_port)
                else:
                    print('all ports exhausted, exiting')
                    exit()
                attempt_count = 0
            # attempt_count += 1
            # if attempt_count > 9:
            #     print('connection failed 10 times, exiting')
            #     exit()

    # loop until get verify back
    while True:
        msg = "verify"
        # message_length = len(msg) ################################################ 
        # client.sendall(message_length.to_bytes(4, byteorder='big'))  # Send the length of the message ################################################
        client.sendall(msg.encode('utf-8')) # send message  
        print('sent verify message, waiting for return')
        incoming = client.recv(1024).decode('utf-8') # recieve message 
        if incoming == 'verify_confirm': # message to confirm verify = "verify_confirm"
            print('recieved verify_confirm')
            break # breaks out of loop when it recieves
    print('connection made, verified connection')









def submit_username_data(client: socket.socket, username: str) -> None:
    '''submits username to the server that gets associated with this clients ip address
    NOTE: USERNAME CAN HAVE NO SPACES, ANY SPACES WILL BE REMOVED'''
    msg = f'username {username}'.encode('utf-8')
    # message_length = len(msg) # chatty
    # client.sendall(message_length.to_bytes(4, byteorder='big')) # chatty
    client.sendall(msg)
    print(f'submitted username to server: {username}')










def request_by_username(client: socket.socket, username: str) -> tuple:
    '''requests an address from the server, getting back an ip address and port'''
    msg = f'request_ip_by_user {username}'.encode('utf-8')
    # print('senttoff msg:', msg)
    client.sendall(msg)
    target_data = client.recv(1024).decode('utf-8')
    if target_data == 'null':
        print('request failed, there is not currently anyone using that username')
        return ('x', 0)
    else:
        # ????????????????????????????????????????
        target_data = target_data.strip('()')
        target_ip, target_port = target_data.split(',')
        target_ip = target_ip.strip().strip("'")
        target_port = target_port.strip()
        target_port = int(target_port)
        print(f'acquired ip and port of {username}, respectively: {target_ip}, {target_port}')
        return (target_ip, target_port)







# port = valid_ports[0]
for port in valid_ports:
    server_port = port
    main_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('CLIENT: CONNECTING TO PORT', port)
    connect_to_server(main_client)
    submit_username_data(main_client, 'SketchedDoughnut')
    time.sleep(1) # NECESSARY OR MESSAGES GET SCRAMBLED AND CUT OFF BY EACHOTHER
    target_ip, target_port = request_by_username(main_client, 'SketchedDoughnut')
    time.sleep(1)