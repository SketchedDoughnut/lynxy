'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION

consider:
- https://wiki.python.org/moin/UdpCommunication
- https://wiki.python.org/moin/TcpCommunication
- https://pythontic.com/modules/socket/udp-client-server-example
- https://www.geeksforgeeks.org/python-simple-port-scanner-with-sockets/
- https://www.geeksforgeeks.org/python-binding-and-listening-with-sockets/
- making decorators for when someone else wants to connect
'''

# included modules
import socket
import random

# files
from .sec import Sec
from .exceptions import Exceptions

####################################################

# this is the main class for the connection
class Comm:
    def __init__(self, host: str, port: int, UDP_bind: bool):
        # this is an instance of the security manager
        self.sec = Sec()
        # this is the internal client used for sending and recieving
        self.host = host
        self.port = port
        # this is the target info
        self.target = ('', 0)
        # this is the client for UDP for finding out who goes first
        self.UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        # this is the main client for communication
        self.TCP_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        # this represents if the UDP client is binded or not
        self.UDP_binded = False
        ###########################################################
        # if UDP_bind, immediately bind to host and port
        if UDP_bind: 
            self.UDP_client.bind((self.host, self.port))
            self.UDP_binded = True


    # this regenerates the UDP client
    def _regen_UDP(self) -> None: self.UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    # this regenerates the TCP client
    def _regen_TCP(self) -> None: self.TCP_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # this function handles the UDP connection that helps make the TCP connection
    def TCP_connect(self, target_ip: str, target_port: int) -> None:
        # set target machine data
        self.target = (target_ip, target_port)
        # we use UDP to get the random number
        ourRandom, targetRandom = self.UDP_connect()
        # we then find out whether to bind our TCP
        # or try to connect to the other end
        # meaning we bind
        self._regen_TCP()
        if ourRandom < targetRandom:
            self.TCP_client.bind((self.host, self.port))
            self.TCP_client.listen(1)
            self.TCP_client, self.target = self.TCP_client.accept()
        # meaning we connect
        elif ourRandom > targetRandom: self.TCP_client.connect(self.target)
        # meaning we cry
        elif ourRandom == targetRandom:
            raise Exceptions.ConnectionFailedError('The handshake between the two machines failed.')
        return None


    # this function manages finding out who goes first with making a TCP connection
    # and also who is first with exchangin keys
    def UDP_connect(self) -> tuple[int, int]:
        # first, we bind to our port / ip if not already
        self._regen_UDP()
        if not self.UDP_binded: 
            self.UDP_client.bind((self.host, self.port))
            self.UDP_binded = True
        # now, we generate and send a random number
        randNum = f'{random.randint(0, 50) + random.randint(0, 50)}'.encode()
        self.UDP_client.sendto(randNum, self.target)
        # now we wait for a number in return, then decode it
        data, self.target = self.UDP_client.recvfrom(1024)
        incomingNum = int(data.decode())
        # we close our UDP and return
        self.UDP_client.close()
        return (randNum, incomingNum)