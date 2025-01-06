import socket
import random
import time
import threading

valid_ports = [
    11111,
    12111,
    11211,
    11121,
    11112
]


# set limit for server instances
INSTANCE_LIMIT = 5
initial_limit_print = False
alive_bound_instance = 0
alive_searching_instance = 0

# create server object, set port
#main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# port = 11111
# port_iter = 0 
# valid_ports = v.valid_ports
not_inclusive_max_port_amount = len(valid_ports) - 1
port = valid_ports[0]

# set up client dict, storing name to ip correlation
client_dict = {
    'default': 0
}

unique_server_instance_dict = {}
message_lookup = {}




# def recv_all(client_socket, n): ################################################
#     # Helper function to receive n bytes or return None if EOF is hit
#     data = bytearray()
#     while len(data) < n:
#         packet = client_socket.recv(n - len(data))
#         if not packet:
#             return None
#         data.extend(packet)
#     return data





# connect to client
def connect_to_client(server: socket.socket, return_port: bool = False) -> list[socket.socket, str, int]:
    global port
    local_port = port
    # bind to first incoming ip, and port
    #server.bind(('', port))
    #print(f'server binded to port {port}')
    while True:
        try:
            print(f'[unbound] attempting to bind to port:', local_port)
            server.bind(('', local_port))
            print(f'[{local_port}] server binded to port {local_port}')
            break
        except:
            if valid_ports.index(local_port) < not_inclusive_max_port_amount:
                print('[unbound] port bind failed, cycling')
                local_port = valid_ports[valid_ports.index(local_port) + 1]
                print('[unbound] swapped to port', local_port)
            else:
                print('[unbound] all ports are being used, cancelling attempt')
                exit()
    print(f'[{local_port}] cycling port ({port}) to local_port ({local_port})')
    port = local_port

    # listen for an incoming connection
    print(f'[{local_port}] server listening for a connection...')
    server.listen(5)

    # set client, client address
    client, addr = server.accept()
    print(f'[{local_port}] connected to client at address {addr}')




    # waits for verification message
    msg = client.recv(1024).decode('utf-8')
    # msg = recv_all(client, 4) ################################################
    # message_length = int.from_bytes(msg, byteorder='big') ################################################
    # msg = recv_all(client, message_length).decode('utf-8') ################################################




    if 'verify' in msg:
        print(f'[{local_port}] recieved "verify" message, sending "verify_confirm"')
        msg = "verify_confirm".encode('utf-8')
        client.sendall(msg)
        print(f'[{local_port}] message sent')
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
        for por in valid_ports:
            try:
                data = unique_server_instance_dict[port]
                state = data[0]
                server_obj = data[1]
                client_obj = data[2]
                closed = is_socket_closed(client_obj)
                if closed == True:
                    print(f'[ALIVE SCANNER] the client for port {por} is not responsive, so the connection will be terminated.')
                    unique_server_instance_dict[por] = [False, server_obj, client_obj]
                # else:
                    # print(f'{por} is connected to a client and healthy')
            except:
                pass
                # print('not checking this port as they have not signed on yet')
        time.sleep(5)
        







# https://stackoverflow.com/questions/48024720/python-how-to-check-if-socket-is-still-connected
def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        #data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        data = sock.recv(16)
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
#def log_username_data(username: str, address: str, c_dict: dict) -> dict:
def log_username_data(username: str, address: str, po: int) -> None:
    global client_dict
    client_dict[username] = address
    print(f'[{po}] logged username ({username})  and address ({address}) to client dict')
    #return client_dict














def answer_request_by_username(client: socket.socket, client_addr: str, server_po: int, c_dict: dict, cmd: str) -> None:
    # cmd = client.recv(1024).decode('utf-8')
    # split_cmd = cmd.split()
    if cmd:
        # if split_cmd[0] == 'request_ip_by_user':
        #     split_cmd.remove('request_ip_by_user')
            # username = "".join(split_cmd)
            username = cmd
            print(f'[{server_po}] client requested data associated with "{username}", searching for in client_dict...')
            try:
                req_details = str(c_dict[username])
                print(f'[{server_po}] data acquired by username: {req_details}')
                msg = req_details.encode('utf-8')
                # client.sendall(msg)
                client.sendto(msg, client_addr)
                print(f'[{server_po}] address sent back to client')
            except:
                print(f'[{server_po}] username does not exist in database, returning None.')
                msg = 'null'.encode('utf-8')
                client.sendall(msg)






# def log_message(client: socket.socket, sport: int) -> None:
#     global message_lookup
#     client.settimeout(5)
#     while True:
#         try:
#             msg = client.recv(1024).decode('utf-8')
#             message_lookup[sport] = msg
#             print('picked up and logged msg')
#             print('-------------------', msg)
#         except:
#             # print('timed out')
#             pass







# MAIN MESSAGE HANDLER
def input_handler(client: socket.socket, client_address: str, server: socket.socket, server_port: int) -> None:
    global client_dict, alive_bound_instance #, message_lookup
    print('----------------------')
    print(f'[{server_port}] INPUT HANDLER STARTED')
    print('----------------------')
    print(f'[{server_port}] starting alive check loop...')
    threading.Thread(target=lambda:check_alive(), daemon=True).start()
    #threading.Thread(target=lambda:log_message(client, server_port), daemon=True).start()
    while True: 
        if unique_server_instance_dict[server_port][0] == False:
            print(f'[{server_port}] this server on port {server_port} has no active client, and will therefore terminate its process')
            # try:
            #     server.shutdown(socket.SHUT_RDWR)
            #     client.shutdown(socket.SHUT_RDWR)
            # except:
            #     pass
            # server.detach()
            # client.detach()
            server.close()
            client.close()
            alive_bound_instance -= 1
            break
        try:
            msg = client.recv(1024).decode('utf-8')
        except:
            print(f'[{server_port}] client has been closed on port {server_port}, server instance terminating')
            # try:
            #     server.shutdown(socket.SHUT_RDWR)
            #     client.shutdown(socket.SHUT_RDWR)
            # except:
            #     pass
            # server.detach()
            # client.detach()
            server.close()
            client.close()
            alive_bound_instance -= 1
            break
        # try:
            #msg = message_lookup[server_port]
        if msg:
            split_msg = str(msg).split()
            print('---------------- MSG', msg)
            print('----------------SPLIT MSG', split_msg)
            prefix = split_msg[0]
            if prefix == 'username':
                print(f'[{server_port}] -- username prefix detected')
                split_msg.remove(prefix)
                username = "".join(split_msg)
                #client_dict = log_username_data(username, client_address, client_dict)
                log_username_data(username, client_address, server_port)
                # message_lookup[server_port] = ''
            elif prefix == 'request_ip_by_user':
                print(f'[{server_port}] -- request_ip_by_user prefix detected')
                split_msg.remove(prefix)
                username = "".join(split_msg)
                answer_request_by_username(client, client_address, server_port, client_dict, username)
                # message_lookup[server_port] = ''
        # except:
            # pass
    exit()







def start_server_instance(server: socket.socket, instance_at_start: int) -> None:
    global alive_searching_instance, alive_bound_instance, unique_server_instance_dict
    print(f'[SERVER STARTER] starting a new searching instance with num: {instance_at_start}')
    main_client, client_address, server_port = connect_to_client(server, return_port=True)
    print('[SERVER STARTER] binded to client, decreasing search and increasing bound')
    alive_searching_instance -= 1
    alive_bound_instance += 1
    print('[SERVER STARTER] bound is now:', alive_bound_instance)
    print('[SERVER STARTER] signing in to active dict with port, logging True and main_client')
    print(f'[SERVER STARTER] client address, server port: {client_address}, {server_port}')
    # active_instance_dict[server_port] = [True, main_client]
    unique_server_instance_dict[server_port] = [True, server, main_client]
    # print('logging client address to detect if closed later')
    # unique_server_instance_dict[main_client] = True
    print('[SERVER STARTER] transferring to input handler') 
    input_handler(main_client, client_address, server, server_port)







def start_instance_handler() -> None:
    global alive_searching_instance, alive_bound_instance, initial_limit_print
    while True:
        if alive_searching_instance == 0:
            if alive_bound_instance < INSTANCE_LIMIT:
                initial_limit_print = False
                print(f'[SERVER HANDLER] starting instance, searching count is {alive_searching_instance} (before)')
                alive_searching_instance += 1
                print(f'[SERVER HANDLER] starting instance, searching count is {alive_searching_instance} (after)')

                main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # main_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 1
                threading.Thread(target=lambda:start_server_instance(main_server, alive_bound_instance + 1), daemon=True).start()
            else:
                if initial_limit_print == False:
                    time.sleep(3) # time for other things to calm down
                    print('[SERVER HANDLER] INSTANCE LIMIT REACHED, NO MORE INSTANCES WILL BE MADE')
                    print('[SERVER HANDLER] BOUND COUNT:', alive_bound_instance)
                    initial_limit_print = True









# start normal handler
start_instance_handler()