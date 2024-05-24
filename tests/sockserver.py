import socketserver

# https://nora.codes/tutorial/socketserver-the-python-networking-module-you-didnt-know-you-needed/
class CaaSHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(b"Enter some data to be capitalized:\n")
        data = self.rfile.readline()
        self.wfile.write(data.upper())

if __name__ == "__main__":
    server = socketserver.TCPServer(('', 11111), CaaSHandler)
    server.serve_forever()


'''
https://pymotw.com/2/SocketServer/
https://stackoverflow.com/questions/37689518/python-socketserver-or-socket-with-thread
https://docs.python.org/3/library/socketserver.html
https://gist.github.com/pklaus/c4c37152e261a9e9331f
https://www.bogotobogo.com/python/python_network_programming_socketserver_framework_for_network_servers.php#google_vignette
https://stackoverflow.com/questions/18563664/socketserver-python
https://realpython.com/courses/python-sockets-part-1/
'''