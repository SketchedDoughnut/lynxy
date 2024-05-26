# a function for submitting username data to the server
def submit_username_data(client: socket.socket, message: str) -> None:
    # local override for package form
    client = main_client
    encoded_message  = message.encode('utf-8')
    client.sendall(encoded_message)
    print(f"Sent:     {message}")
    incoming_data = client.recv(1024).decode('utf-8')
    print(f"Received: {incoming_data}")

# requests ip and port from server
def request_username_data(client: socket.socket, message: str) -> socket.socket:
    encoded_message = message.encode('utf-8')
    client.sendall(encoded_message)
    print(f"Sent:     {message}")
    # incoming_data = full_recieve(client)
    incoming_data = client.recv(1024).decode('utf-8')
    print(f"Received: {incoming_data}")