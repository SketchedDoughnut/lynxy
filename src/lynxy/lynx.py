import socket

# set up server ip, port to connect to
server_ip = input('enter ip: ')
server_port = 12345
# start client object
main_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connects to server
def connect_to_server(client: socket.socket):
    '''sets up the initial connection to the server, verifies it can send data over'''
    
    # connect to server ip, server port
    print('cycling connection to server until succeed / fail...')
    attempt_count = 0
    while True:
        print(f'attempt: {attempt_count}')
        try:
            client.connect((server_ip, server_port))
            print('connected to server')
            break
        except:
            attempt_count += 1
            if attempt_count > 9:
                print('connection failed 10 times, exiting')
                exit()

    # loop until get verify back
    while True:
        msg = "verify"
        client.send(msg.encode('utf-8')) # send message 
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
    client.send(msg)
    print('submitted username to server')

def request_by_username(client: socket.socket, username: str) -> str:
    '''requests an address from the server, getting back an ip address and port'''
    msg = f'request_ip_by_user {username}'.encode('utf-8')
    client.send(msg)
    target_data = client.recv(1024).decode('utf-8')
    if target_data == 'null':
        print('request failed, there is not currently anyone using that username')
    else:
        # ????????????????????????????????????????
        target_data = target_data.strip('()')
        target_ip, target_port = target_data.split(',')
        target_ip = target_ip.strip().strip("'")
        target_port = target_port.strip()
        target_port = int(target_port)
        print(f'acquired ip and port, respectively: {target_ip}, {target_port}')




connect_to_server(main_client)
submit_username_data(main_client, 'SketchedDoughnut')
request_by_username(main_client, 'SketchedDoughnut')