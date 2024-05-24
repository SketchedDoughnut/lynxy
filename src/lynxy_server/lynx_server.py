import socketserver
import socket

client_dict = {
    'default': 0
}

valid_ports = [
    11111,
    12111,
    11211,
    11121,
    11112,
    22111,
    12211,
    11221,
    11122,
    22222
]

HOST = '' # localhost
PORT = valid_ports[0]



class myTCPserver(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        global client_dict
        while True:
            msg = bytes(self.request.recv(1024)).decode('utf-8')
            split_msg = msg.split()
            prefix = split_msg[0]
            split_msg.remove(prefix)
            joined_msg = "".join(split_msg)

            # print(f"{self.client_address[0]} wrote: {msg}")

            if prefix == 'username':
                client_dict[joined_msg] = self.client_address
                print(f'[{self.client_address[0]}] {prefix} - logging {self.client_address} to {joined_msg}')
                self.request.sendall('logged username, data'.encode('utf-8'))

            elif prefix == 'request_by_user':
                try:
                    self.request.sendall(str(client_dict[joined_msg]).encode('utf-8'))
                    print(f'[{self.client_address[0]}] {prefix} - return {joined_msg} data: {client_dict[joined_msg]}')
                except:
                    pass

            elif msg == 'end_session':
                self.request.sendall('ending'.encode('utf-8'))
                print(f'[{self.client_address[0]}] {msg} - ending this instance')
                print('----------------------------------------------')
                break

            else:
                self.request.sendall(msg.upper().encode('utf-8'))  # Send response back to the client




def cycle_start() -> None:
    global PORT
    connected = False
    for port in valid_ports:

        try:
            print(f'[PORT CYCLE] Server trying port: {port}')
            with socketserver.ThreadingTCPServer((HOST, port), myTCPserver) as server:
                print(f'[PORT CYCLE] Server found port for startup: {port}')
                print('----------------------------------------------')
                connected = True
                PORT = port
                server.serve_forever()
                break
        except IndexError:
            port = valid_ports[0]
            print(f'[PORT CYCLE - RESET 1] Server resetting port to: {port}')
        except:
            try:
                print(f'[PORT CYCLE] Server port cycling: {port} -> {valid_ports[valid_ports.index(port) + 1]}')
            except IndexError:
                port = valid_ports[0]
                print(f'[PORT CYCLE - RESET 2] Server resetting port to: {port}')
    
    if connected == False:
        print('Server failed to find an open valid port, exiting')
        exit()