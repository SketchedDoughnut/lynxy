'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION

consider:
- https://wiki.python.org/moin/UdpCommunication
- https://wiki.python.org/moin/TcpCommunication
- https://pythontic.com/modules/socket/udp-client-server-example
- https://www.geeksforgeeks.org/python-simple-port-scanner-with-sockets/
- https://www.geeksforgeeks.org/python-binding-and-listening-with-sockets/
- making decorators for when someone else wants to connect
- https://stackoverflow.com/questions/2470971/fast-way-to-test-if-a-port-is-in-use-using-python
'''

# included modules
import socket
import random
import time

# external modules
import psutil

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
        if len(host) > 0: self.host = host
        else: self.host = socket.gethostbyname(socket.gethostname())
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


    # this returns the host IP
    def get_host(self) -> tuple[str, int]: return self.host, self.port

    
    # this function handles the UDP connection that helps make the TCP connection
    def TCP_connect(self, target_ip: str, target_port: int, timeout: int = 10, attempts: int = 6) -> None:
        # set target machine data
        self.target = (target_ip, target_port)

        print('set target to:', self.target) #################################################

        # we use UDP to get the random number
        ourRandom, targetRandom = self.UDP_connect(timeout, attempts)
        # we then find out whether to bind our TCP
        # or try to connect to the other end
        self._regen_TCP()

        print(f'{ourRandom}, {targetRandom}') #################################################

        # meaning we bind
        if ourRandom < targetRandom:
            # self.TCP_client.bind((self.host, self.port))
            # self.TCP_client.listen(1)
            # self.TCP_client, self.target = self.TCP_client.accept()

            print('im second!') #################################################

        # meaning we connect
        elif ourRandom > targetRandom: 
            # self.TCP_client.connect(self.target)

            print('im first!') #################################################
        
        print('connected!') #################################################

        return None


    # this function manages finding out who goes first with making a TCP connection
    # and also who is first with exchangin keys
    def UDP_connect(self, timeout, attempts) -> tuple[int, int]:
        # first, we bind to our port / ip if not already
        if not self.UDP_binded: 
            self._regen_UDP()
            self.UDP_client.bind((self.host, self.port))
            self.UDP_binded = True
        # now, we generate and send a random number
        randNum = random.randint(0, 100) + random.randint(0, 100)
        # we try "attempts" times to connect and wait "timeout" seconds for a response
        connectionSuccess = False
        self.UDP_client.settimeout(timeout)
        for attemptNum in range(attempts):
            print('attempt:', attemptNum) #################################################
            try:
                # if we send the data and get data back,
                # then it succeeded
                self.UDP_client.sendto(str(randNum).encode(), self.target)
                data, self.target = self.UDP_client.recvfrom(1024)
                self.UDP_client.sendto(str(randNum).encode(), self.target) # make sure data got through

                # TODO
                # we decode the incoming value to make sure the two values aren't equal
                # if they are, we regen number and keep trying
                
                incomingNum = int(data.decode())
                # otherwise connection was a success, break
                connectionSuccess = True
                break
            except TimeoutError:

                print('Timeout: Retrying...') #################################################

        # if no success, raise error
        if not connectionSuccess: raise Exceptions.ConnectionFailedError('The target port is not in use by another machine.')
        # we close our UDP and return
        self.UDP_client.close()
        return (randNum, incomingNum)
    

    # this function closes the connection between the two machines
    def close_connection(self) -> None: 
        self.TCP_client.close()
        self._regen_UDP()
        self._regen_TCP()
        self.UDP_binded = False
        return