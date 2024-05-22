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
# active_instance_dict = {}

# connect to client
def connect_to_client(server: socket.socket, return_port: bool = False) -> list[socket.socket, str, int]:
    global port
    local_port = port
    # bind to first incoming ip, and port
    #server.bind(('', port))
    #print(f'server binded to port {port}')
    while True:
        try:
            print('attempting to bind to port:', local_port)
            server.bind(('', local_port))
            print(f'server binded to port {local_port}')
            break
        except:
            if valid_ports.index(local_port) < not_inclusive_max_port_amount:
                print('port bind failed, cycling')
                local_port = valid_ports[valid_ports.index(local_port) + 1]
                print('swapped to port', local_port)
            else:
                print('all ports are being used, cancelling attempt')
                exit()
    port = local_port

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
        if return_port == True:
            return [client, addr, local_port]
        else:
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










def check_alive() -> None:
    global unique_server_instance_dict
    import time
    while True:
        time.sleep(5)
        for por in valid_ports:
            try:
                data = unique_server_instance_dict[port]
                state = data[0]
                server_obj = data[1]
                client_obj = data[2]
                state = is_socket_closed(client_obj)
                if state == True:
                    print(f'the client for port {por} is not responsive, so the connection will be terminated.')
                    unique_server_instance_dict[por] = [False, server_obj, client_obj]
            except:
                pass
        







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
def input_handler(client: socket.socket, client_address: str, server: socket.socket, server_port: int) -> None:
    global client_dict, alive_bound_instance
    print('----------------------')
    print('INPUT HANDLER STARTED')
    print('----------------------')
    print('starting alive check loop...')
    threading.Thread(target=lambda:check_alive()).start()
    while True: 
        if unique_server_instance_dict[server_port][0] == False:
            print(f'this server on port {server_port} has no active client, and will therefore terminate its process')
            server.close()
            client.close()
            alive_bound_instance -= 1
            exit()
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
    main_client, client_address, server_port = connect_to_client(server, return_port=True)
    print('binded to client, decreasing search and increasing bound')
    alive_searching_instance -= 1
    alive_bound_instance += 1
    print('bound is now:', alive_bound_instance)
    print('signing in to active dict with port, logging True and main_client')
    # active_instance_dict[server_port] = [True, main_client]
    unique_server_instance_dict[server_port] = [True, server, main_client]
    # print('logging client address to detect if closed later')
    # unique_server_instance_dict[main_client] = True
    print('transferring to input handler')
    input_handler(main_client, client_address, server, server_port)







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









# start normal handler
start_instance_handler()