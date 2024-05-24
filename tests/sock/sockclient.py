# import socket

# ip = '' # localhost
# port = 1111

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# input('input to start: ')
# client.connect((ip, port))
# client.sendall('message from client!'.encode('utf-8'))
# print(client.recv(1024).decode('utf-8'))

import socket

HOST, PORT = "localhost", 11111

for i in range(2):
    # data = f"Hello, World: {i}"
    data = f'request_by_user SketchedDoughnut-{i}'
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(data.encode('utf-8'))

        # Receive data from the server and shut down
        received = sock.recv(1024)

    print(f"Sent:     {data}")
    print(f"Received: {received.decode('utf-8')}")