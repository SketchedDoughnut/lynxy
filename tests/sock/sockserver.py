import socketserver

client_dict = {
    'default': 0
}


class myTCPserver(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        global client_dict
        msg = bytes(self.request.recv(1024)).decode('utf-8')
        print(f"{self.client_address[0]} wrote:")
        print(msg)
        split_msg = msg.split()
        if split_msg[0] == 'username':
            split_msg.remove(split_msg[0])
            msg = "".join(split_msg)
            client_dict[msg] = self.client_address
        elif split_msg[0] == 'request_by_user':
            split_msg.remove(split_msg[0])
            msg = "".join(split_msg)
            self.request.sendall(str(client_dict[msg]).encode('utf-8'))
        else:
            self.request.sendall(msg.upper().encode('utf-8'))  # Send response back to the client

host = '' # localhost
port = 11111 
with socketserver.ThreadingTCPServer((host, port), myTCPserver) as server:
    server.serve_forever()