import socket
import random
import threading

# set limit for server instances
INSTANCE_LIMIT = 5
alive_bound_instance = 0
alive_searching_instance = 0

# create server object, set port
#main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 11111
port_iter = 0

# set up client dict, storing name to ip correlation
client_dict = {
    'default': 0
}

# connect to client
def connect_to_client(server: socket.socket) -> list[socket.socket, str]:
    global port_iter
    # bind to first incoming ip, and port
    #server.bind(('', port))
    #print(f'server binded to port {port}')
    n_port = int(int(port) + int(port_iter))
    print('attempting to bind to port:', n_port)
    server.bind(('', n_port))
    print(f'server binded to port {n_port}')
    print('connected to port, port iter incremented')
    port_iter += 1

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
    global client_dict
    print('----------------------')
    print('INPUT HANDLER STARTED')
    print('----------------------')
    while True: 
        # passed = False
        # try:
        #     msg = client.recv(1024).decode('utf-8')
        #     passed = True
        # except:
        #     print('error listening from client, re-connecting to any ip...')
        #     main_client, client_address = connect_to_client(main_server)
        # if passed == True:
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







def server_instance(server: socket.socket, instance_at_start: int) -> None:
    print(f'starting a new searching instance with num: {instance_at_start}')
    global alive_searching_instance, alive_bound_instance
    main_client, client_address = connect_to_client(server)
    print('binded to client, decreasing search and increasing bound')
    alive_searching_instance -= 1
    alive_bound_instance += 1
    print('bound is now:', alive_bound_instance)
    print('transferring to input handler')
    input_handler(main_client, client_address)



def start_instance() -> None:
    global alive_searching_instance, alive_bound_instance
    while True:
        if alive_searching_instance == 0:
            print(f'starting instance, searching count is {alive_searching_instance}')
            alive_searching_instance += 1
            main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            threading.Thread(target=lambda:server_instance(main_server, alive_bound_instance + 1), daemon=True).start()
            #break


start_instance()


while True:
    pass