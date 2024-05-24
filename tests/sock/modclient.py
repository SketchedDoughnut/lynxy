# import socket

# ip = '' # localhost
# port = 1111

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# input('input to start: ')
# client.connect((ip, port))
# client.sendall('message from client!'.encode('utf-8'))
# print(client.recv(1024).decode('utf-8'))

# this below code has been contributed to by chat gpt
import socket

HOST, PORT = "localhost", 11111
sock_list = []
for i in range(100):
    sock_list.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                     )
# for i in range(2):
count = 0
for sock in sock_list:
    # data = f"Hello, World: {i}"
    data = f'request_by_user SketchedDoughnut-{count}'
    count += 1
    # Create a socket (SOCK_STREAM means a TCP socket)
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data.encode('utf-8'))

    # Receive data from the server and shut down
    received = sock.recv(1024)

    print(f"Sent:     {data}")
    print(f"Received: {received.decode('utf-8')}")