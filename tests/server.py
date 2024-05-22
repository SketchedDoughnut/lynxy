import socket
import random
import threading

# file imoprts
import valid_ports as v


# set limit for server instances
INSTANCE_LIMIT = 5
initial_limit_print = False
alive_bound_instance = 0
alive_searching_instance = 0

# create server object, set port
#main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# port = 11111
# port_iter = 0
valid_ports = v.valid_ports
not_inclusive_max_port_amount = len(valid_ports) - 1
port = valid_ports[0]

# set up client dict, storing name to ip correlation
client_dict = {
    'default': 0
}

unique_server_instance_dict = {}
# active_dict = {}
# for i in range(INSTANCE_LIMIT):
#     active_dict[i] = False

# def start_info_handler() -> None:
#     info_port = 22222
#     while True:
#         info_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         print('info server made')
#         info_server.bind(('', info_port))
#         print('info server binded to port', info_port)
#         info_server.listen(5)
#         print('info server listening')
#         info_client, info_client_address = info_server.accept()
#         print('info server accepted from:', info_client_address)
#         msg = f'{active_dict}'.encode('utf-8')
#         info_client.send(msg)
#         print('message sent')
#         info_client.close()
#         info_server.close()
#         print('info client, info_server closed')

# connect to client
def connect_to_client(server: socket.socket) -> list[socket.socket, str]:
    global port
    # bind to first incoming ip, and port
    #server.bind(('', port))
    #print(f'server binded to port {port}')
    while True:
        try:
            print('attempting to bind to port:', port)
            server.bind(('', port))
            print(f'server binded to port {port}')
            break
        except:
            if valid_ports.index(port) < not_inclusive_max_port_amount:
                print('port bind failed, cycling')
                port = valid_ports[valid_ports.index(port) + 1]
                print('swapped to port', port)
            else:
                print('all ports are being used, cancelling attempt')
                exit()

    # listen for an incoming connection
    print('server listening for a connection...')
    server.listen(5)

    # set client, client address
    client, addr = server.accept()
    print(f'connected to client at address {addr}')

    # waits for verification message
    msg = client.recv(1024).decode('utf-8')
    if 'verify' in msg:
        print('recieved "verify" message, sending "verify_confirm"')
        msg = "verify_confirm".encode('utf-8')
        client.send(msg)
        print('message sent')
        return [client, addr]

# intake username data
# def recieve_username_data(client: socket.socket, msg: str) -> str:
#     # msg = client.recv(1024).decode('utf-8')
#     split_msg = msg.split()
#     if msg:
#         if split_msg[0] == "username":
#             split_msg.remove("username")
#             username = "".join(split_msg)
#             print(f'username recieved: {username}')
#             return username

def check_alive(client: socket.socket) -> bool:
    global unique_server_instance_dict
    import time
    time.sleep(5)
    state = is_socket_closed(client)
    if state == True:
        print('socket has been detected as dead, changing state to dead (false)')
        unique_server_instance_dict[client] = False
        client.close()
    
# https://stackoverflow.com/questions/48024720/python-how-to-check-if-socket-is-still-connected
def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e:
        #logger.exception("unexpected exception when checking if a socket is closed")
        return False
    return False

# log username data into client_dict
def log_username_data(username: str, address: str, c_dict: dict) -> dict:
    c_dict[username] = address
    print('logged username and address to client dict')
    return c_dict

def answer_request_by_username(client: socket.socket, c_dict: dict, cmd: str) -> None:
    # cmd = client.recv(1024).decode('utf-8')
    # split_cmd = cmd.split()
    if cmd:
        # if split_cmd[0] == 'request_ip_by_user':
        #     split_cmd.remove('request_ip_by_user')
            # username = "".join(split_cmd)
            username = cmd
            print(f'client requested data associated with "{username}", searching for in client_dict...')
            try:
                req_details = str(c_dict[username])
                print(f'data acquired by username: {req_details}')
                msg = req_details.encode('utf-8')
                client.send(msg)
                print('address sent back to client')
            except:
                print('username does not exist in database, returning None.')
                msg = 'null'.encode('utf-8')
                client.send(msg)















# MAIN MESSAGE HANDLER
def input_handler(client: socket.socket, client_address: str) -> None:
    global client_dict, alive_bound_instance
    print('----------------------')
    print('INPUT HANDLER STARTED')
    print('----------------------')
    # print('starting ping thread...')
    # threading.Thread(target=lambda:check_alive(client), daemon=True).start()
    while True: 
        # passed = False
        # try:
        #     msg = client.recv(1024).decode('utf-8')
        #     passed = True
        # except:
        #     print('error listening from client, re-connecting to any ip...')
        #     main_client, client_address = connect_to_client(main_server)
        # if passed == True:
        # if unique_server_instance_dict[client] == False:
        #     print('client has been deemed dead, killing')
        #     client.close()
        #     alive_bound_instance -= 1
        #     print('bound count changed to', alive_bound_instance)
        #     print('searching count is', alive_searching_instance)
        #     print('current unique dict:', unique_server_instance_dict)
        #     exit()
        msg = client.recv(1024).decode('utf-8')
        if msg:
            split_msg = msg.split()
            prefix = split_msg[0]
            if prefix == 'username':
                print('-- username prefix detected')
                split_msg.remove(prefix)
                username = "".join(split_msg)
                client_dict = log_username_data(username, client_address, client_dict)
            elif prefix == 'request_ip_by_user':
                print('-- request_ip_by_user prefix detected')
                split_msg.remove(prefix)
                username = "".join(split_msg)
                answer_request_by_username(client, client_dict, username)







def start_server_instance(server: socket.socket, instance_at_start: int) -> None:
    print(f'starting a new searching instance with num: {instance_at_start}')
    global alive_searching_instance, alive_bound_instance, unique_server_instance_dict
    main_client, client_address = connect_to_client(server)
    print('binded to client, decreasing search and increasing bound')
    alive_searching_instance -= 1
    alive_bound_instance += 1
    print('bound is now:', alive_bound_instance)
    print('logging client address to detect if closed later')
    unique_server_instance_dict[main_client] = True
    print('transferring to input handler')
    input_handler(main_client, client_address)







def start_instance_handler() -> None:
    global alive_searching_instance, alive_bound_instance, initial_limit_print
    while True:
        if alive_searching_instance == 0:
            if alive_bound_instance < INSTANCE_LIMIT:
                initial_limit_print = False
                print(f'starting instance, searching count is {alive_searching_instance}')
                alive_searching_instance += 1
                main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                threading.Thread(target=lambda:start_server_instance(main_server, alive_bound_instance + 1), daemon=True).start()
            else:
                if initial_limit_print == False:
                    import time
                    time.sleep(3) # time for other things to calm down
                    print('INSTANCE LIMIT REACHED, NO MORE INSTANCES WILL BE MADE')
                    print('BOUND COUNT:', alive_bound_instance)
                    initial_limit_print = True



# start info handler
# start_info_handler()

# start normal handler
start_instance_handler()