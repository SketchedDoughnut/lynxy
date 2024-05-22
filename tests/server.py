import socket

# create server object, set port
main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345

# set up client dict, storing name to ip correlation
client_dict = {}

# connect to client
def connect_to_client(server: socket.socket) -> list[socket.socket, str]:
    # bind to first incoming ip, and port
    server.bind(('', port))
    print(f'server binded to port {port}')

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
def recieve_username_data(client: socket.socket) -> str:
    msg = client.recv(1024).decode('utf-8')
    split_msg = msg.split()
    if split_msg[0] == "username":
        split_msg.remove("username")
        username = "".join(split_msg)
        print(f'username recieved: {username}')
        return username

# log username data into client_dict
def log_username_data(username: str, address: str, c_dict: dict) -> None:
    c_dict[username] = address
    print('logged username and address to client dict')
    return c_dict

def answer_request_by_username(client: socket.socket, c_dict: dict) -> None:
    cmd = client.recv(1024).decode('utf-8')
    split_cmd = cmd.split()
    if split_cmd[0] == 'request_ip_by_user':
        split_cmd.remove('request_ip_by_user')
        username = "".join(split_cmd)
        print(f'client requested {username}s data, searching for in client_dict...')
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


# run
main_client, client_address = connect_to_client(main_server)
username = recieve_username_data(main_client)
client_dict = log_username_data(username, client_address, client_dict)
answer_request_by_username(main_client, client_dict)