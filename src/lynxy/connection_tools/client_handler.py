import socket 

def client_start() -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client

def server_connect(client: socket.socket, ip: str):
    client.connect(ip)

def client_listen(client: socket.socket)