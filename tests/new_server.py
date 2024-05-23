import socket
import random
import time
import threading

# all valid ports to cycle through
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

# set port limits, defaults
not_inclusive_max_port_amount = len(valid_ports) - 1
default_port = valid_ports[0]

# set up client dict, storing username to ip correlation
client_dict = {
    'default': 0
}

# a dictionary where a port number is associated with [State of living (bool), server_socket, client_socket] NOTE: server_socket is not used
unique_server_instance_dict = {}
for port in valid_ports:
    unique_server_instance_dict[port] = [False, 'x', 'x']





### FUNCTIONS

## TOOlS
# def 



## CORE FUNCTIONS
# connect to client
def connect_to_client(server: socket.socket, return_port: bool = False) -> list:
    # access global
    local_port = default_port
    
    # while True:
        # try:
        #     # attempt to bind to socket, if succeed, break out of loop
        #     print(f'[unbound] attempting to bind to port:', local_port)
        #     server.bind(('', local_port))
        #     print(f'[{local_port}] server binded to port {local_port}')
        #     break

        # except:
        #     # if socket bind failed, and the current local_port is not at the end of the valid_ports list, then cycle port to the next index in valid_ports
        #     if valid_ports.index(local_port) < not_inclusive_max_port_amount:
        #         print('[unbound] port bind failed, cycling')
        #         local_port = valid_ports[valid_ports.index(local_port) + 1]
        #         print('[unbound] swapped to port', local_port)
            
        #     # if all ports are busy, exit client
        #     else:
        #         print('[unbound] all ports are being used, cancelling attempt')
        #         exit()

    try:
        # iterate through valid ports, check if any are not alive in unique_server_instance_dict
        found_open = False
        for port in valid_ports:
            data = unique_server_instance_dict[port]
            is_alive = data[0]
            server_obj = data[1]
            client_obj = data[2]
            if is_alive == False:
                found_open = True
                open_port = port
                break
        if found_open == True:
            print(f'[unbound] open port found: {open_port}')
            server.bind(('', open_port))
            print(f'[{open_port}] server binded to port {open_port}')
        else:
            print('[unbound] all ports are being used, cancelling attempt')
            exit()
    except Exception as e:
        print(f'[unbound] an error occured when trying to bind to ports: {e}')



    # print(f'[{local_port}] cycling port ({default_port}) to local_port ({local_port})')
    # default_port = local_port

    # listen for an incoming connection
    print(f'[{open_port}] server listening for a connection...')
    server.listen(5)

    # set client, client address
    client, client_address = server.accept()
    print(f'[{open_port}] connected to client at address {client_address}')

    # waits for verification message
    msg = client.recv(1024).decode('utf-8')

    # if verification message contains "verify", return "verify_confirm"
    if 'verify' in msg:
        print(f'[{local_port}] recieved "verify" message, sending "verify_confirm"')
        msg = "verify_confirm".encode('utf-8')
        client.sendall(msg)
        print(f'[{local_port}] verify_confirm sent')
        if return_port == True:
            return [client, client_address , open_port] # if port requested, return client, client_address, and the port used for this instance
        else:
            return [client, client_address] # if no port requested, return client, client_address
        


# logs username data into client_dict (ONE OF THE FEW FUNCTIONS WITH GLOBAL ACCESS TO VARS)
def log_username_data(username: str, address: str, port: int) -> None:
    global client_dict
    client_dict[username] = address
    print(f'[{port}] logged username ({username})  and address ({address}) to client dict')



# answer requests with a username with the data assigned to that username -> ip, port
def answer_request_by_username(client: socket.socket, client_address: str, port: int, client_dict: dict, username: str) -> None:
    # if string not empty, continue
    if username:
        print(f'[{port}] client requested data associated with "{username}", searching for in client_dict...')
        # try to search for that username in the databse
        try:
            req_details = str(client_dict[username])
            print(f'[{port}] data acquired by username: {req_details}')
            msg = req_details.encode('utf-8')
            # client.sendall(msg)
            #client.sendto(msg, client_address)
            print(f'[{port}] address found')

        # if failed, then there is no person of that username, send that back
        except:
            print(f'[{port}] username does not exist in database, returning null')
            msg = 'null'.encode('utf-8')
        client.sendall(msg)
        print(f'[{port}] request results sent back to client')



# handles inputs while scanning for messages (ONE OF THE FEW FUNCTIONS WITH GLOBAL ACCESS TO VARS)
def input_handler(client: socket.socket, client_address: str, server: socket.socket, server_port: int) -> None:
    global client_dict, alive_bound_instance
    # starts
    print(f'----------------------\n[{server_port}] INPUT HANDLER STARTED\n----------------------')

    # starts thread to check for what sockets are alive (disabled, currently) 
    # print(f'[{server_port}] starting alive check loop...') ################################################
    # threading.Thread(target=lambda:check_alive(), daemon=True).start() ################################################

    # main loop
    while True: 
        # see if the current server is supposed to be alive
        is_alive = unique_server_instance_dict[server_port][0]
        if is_alive == False:
            print(f'[{server_port}] this server on port {server_port} has no active client, and will therefore terminate its process')
            # close client and server if this port is not connected to a client
            server.close()
            client.close()
            # lower how many are considered alive and bound so a new instance can be made 
            alive_bound_instance -= 1
            break

        # try to recieve a message from the client
        try:
            msg = client.recv(1024).decode('utf-8')

        # failed due to lack of connection, or whatnot -> close server and client
        except:
            print(f'[{server_port}] client has been closed on port {server_port}, server instance terminating')
            server.close()
            client.close()
            # lower how many are considered alive and bound so a new instance can be made 
            alive_bound_instance -= 1
            break
        
        # if message is not empty, continue
        if msg:
            # split message into a list, see command (list[0], assigned to "prefix")
            split_msg = str(msg).split()
            print('---------------- MSG', msg)
            print('----------------SPLIT MSG', split_msg)
            prefix = split_msg[0]

            # if prefix is username, remove the prefix from the string and re-connect it together
            if prefix == 'username':
                print(f'[{server_port}] -- username prefix detected')
                split_msg.remove(prefix)
                username = "".join(split_msg)
                # call on the function to log username data, passing in -> username, client_address, server_port (just for printing)
                log_username_data(username, client_address, server_port)

            # elif prefix is request_ip_by_user, remove the prefix from the string and re-connect it together
            elif prefix == 'request_ip_by_user':
                print(f'[{server_port}] -- request_ip_by_user prefix detected')
                split_msg.remove(prefix)
                username = "".join(split_msg)
                # call on the function to answer this request, passing in -> client, client_address, server_port, client_dict, username
                answer_request_by_username(client, client_address, server_port, client_dict, username)

    # exit if the code broke out of the loop
    exit()



# this function is called on to set up the initial server instance (thread) (ONE OF THE FEW FUNCTIONS WITH GLOBAL ACCESS TO VARS)
def start_server_instance(instance_at_start: int) -> None:
    global alive_searching_instance, alive_bound_instance, unique_server_instance_dict

    # set up the server object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # main_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ################################################

    # set the client object, the clients address, and the servers binded port from connect_to_client, passing in a server socket
    print(f'[SERVER STARTER] starting a new searching server instance with num: {instance_at_start}')
    client, client_address, server_port = connect_to_client(server, return_port=True)
    print(f'[SERVER STARTER] server instance {instance_at_start} binded to client')

    # sign into the dictionary, passing in -> alive or dead (bool, default is True as we are starting), server socket, client_socket
    print(f'[SERVER STARTER] client address, server port: {client_address}, {server_port}')
    unique_server_instance_dict[server_port] = [True, server, client]
    print('[SERVER STARTER] signing in to active dict with port, logging True and main_client')

    # lower searching as server instance has found client, increase bound (will trigger a new instance creation)
    print('[SERVER STARTER] decreasing search and increasing bound')
    alive_searching_instance -= 1
    alive_bound_instance += 1
    print('[SERVER STARTER] searching is now:', alive_searching_instance)
    print('[SERVER STARTER] bound is now:', alive_bound_instance)

    # start the input handler, this thread has now finished its task
    print('[SERVER STARTER] transferring to input handler') 
    input_handler(client, client_address, server, server_port)



# the manager for starting server instances (ONE OF THE FEW FUNCTIONS WITH GLOBAL ACCESS TO VARS)
def start_instance_handler() -> None:
    global alive_searching_instance, alive_bound_instance, initial_limit_print
    
    # main loop
    while True:
        # if no instances are searching, continue
        if alive_searching_instance == 0:
            # if the amount of bound instances is below the limit, start a new instance (assigned a cosmetic num which is alive_bound_instance + 1)
            if alive_bound_instance < INSTANCE_LIMIT:
                initial_limit_print = False
                # increment alive_bound_instance
                print(f'[SERVER HANDLER] starting instance, searching count is {alive_searching_instance} (before)')
                alive_searching_instance += 1
                print(f'[SERVER HANDLER] starting instance, searching count is {alive_searching_instance} (after)')
                
                # create a var, then immediately start, this gets overwritten when a new one is created
                new_server_thread = threading.Thread(target=lambda:start_server_instance(alive_bound_instance + 1), daemon=True)
                new_server_thread.start()

            # if we are the limit, print taht we are (initial_limit_print used to not spam console) and finish
            else:
                if initial_limit_print == False:
                    time.sleep(3) # time for other things to calm down
                    print(f'[SERVER HANDLER] INSTANCE LIMIT REACHED, NO MORE INSTANCES WILL BE MADE\n[SERVER HANDLER] BOUND COUNT: {alive_bound_instance}')
                    initial_limit_print = True




# the only acting line, calling on the handler which handles everything
start_instance_handler()