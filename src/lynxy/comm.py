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
- https://stackoverflow.com/questions/50216417/why-use-socket-io-and-not-just-socket
- https://github.com/MagicStack/uvloop?tab=Apache-2.0-1-ov-file
- https://stackoverflow.com/questions/27435284/multiprocessing-vs-multithreading-vs-asyncio
- https://stackoverflow.com/questions/34252273/what-is-the-difference-between-socket-send-and-socket-sendall
- https://stackoverflow.com/questions/1708835/python-socket-receive-incoming-packets-always-have-a-different-size
- https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
- https://stackoverflow.com/questions/42415207/send-receive-data-with-python-socket

Info about byte order:
- https://www.ibm.com/docs/ja/zvm/7.2?topic=domains-network-byte-order-host-byte-order
- https://stackoverflow.com/questions/71695996/can-you-give-some-practical-uses-of-socket-ntohlx-in-socket-programming-in
'''

# included modules
import socket
import random
import pickle

# external modules
from rich import print

# files
from .sec import Sec
from .exceptions import Exceptions

####################################################

# this is the main class for the connection
class Comm:
    def __init__(self, host: str, port: int, UDP_bind: bool):
        # this is an instance of the security manager
        self.sec = Sec()
        # this is an instance of the parser
        # this is the internal client used for sending and recieving
        if len(host) > 0: self.host = host
        else: self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        # this is the target info
        self.target = ('', 0)
        # this is the actual connected target info (FOR TCP)
        self.actual_target = ('', 0)
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
    def __regen_UDP(self) -> None: self.UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    # this regenerates the TCP client
    def __regen_TCP(self) -> None: self.TCP_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # this returns the host IP
    def _get_host(self) -> tuple[str, int]: return self.host, self.port


    # this returns the actual target
    # that target being the active TCP connection
    def _get_actual_target(self) -> tuple[str, int]: return self.actual_target

    
    # this function handles the UDP connection that helps make the TCP connection
    def _TCP_connect(self, target_ip: str, target_port: int, timeout: int = 10, attempts: int = 6) -> None:
        # set target machine data
        self.target = (target_ip, target_port)
        # we use UDP to get the random number
        ourRandom, targetRandom = self._UDP_connect(timeout, attempts)
        # we then find out whether to bind our TCP
        # or try to connect to the other end
        self.__regen_TCP()
        # meaning we connect (first)
        if ourRandom > targetRandom: 
            self.TCP_client.connect(self.target)
            self.actual_target = self.target
        # meaning we bind (second)
        elif ourRandom < targetRandom:
            # we try (attempts) times to connect
            # an invalid connection is if the client that connects
            # is not the one we wanted to connect to
            connectionSuccess = False
            for _ in range(attempts):
                self.__regen_TCP()
                self.TCP_client.bind((self.host, self.port))
                self.TCP_client.listen(1) # only listen for 1 connection
                self.TCP_client, connectedTarget = self.TCP_client.accept()
                if connectedTarget[0] == self.target[0]: # verify IP, not port
                    self.actual_target = connectedTarget
                    connectionSuccess = True
                    break
            # raise error if connection failed
            if not connectionSuccess: raise Exceptions.ConnectionFailedError(f'The incorrect target machine connected to this machine {attempts} times.') 
        # do the handshake to exchange RSA keys
        self._handshake(ourRandom > targetRandom)
        return None


    # this function manages finding out who goes first with making a TCP connection
    # and also who is first with exchangin keys
    def _UDP_connect(self, timeout, attempts) -> tuple[int, int]:
        # first, we bind to our port / ip if not already
        if not self.UDP_binded: 
            self.__regen_UDP()
            self.UDP_client.bind((self.host, self.port))
            self.UDP_binded = True
        # now, we generate and send a random number
        randNum = random.randint(0, 1000) + random.randint(0, 1000)
        # we try "attempts" times to connect and wait "timeout" seconds for a response
        connectionSuccess = False
        self.UDP_client.settimeout(timeout)
        for _ in range(attempts):
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
            except TimeoutError: continue

        # if no success, raise error
        if not connectionSuccess: raise Exceptions.ConnectionFailedError('The target port is not in use by another machine.')
        # we close our UDP and return
        self.UDP_client.close()
        return (randNum, incomingNum)
    

    # this function manages handshakes
    def _handshake(self, is_first: bool) -> None:
        if is_first:
            # we send our public key
            self.TCP_client.sendall(pickle.dumps(self.sec.int_pub_key))
            # then recieve their public key
            recievedPubKey = self.TCP_client.recv(1024)
            properPubKey = pickle.loads(recievedPubKey)
            self.sec.load_RSA(properPubKey)
        else:
            # we recieve their public key
            recievedPubKey = self.TCP_client.recv(1024)
            properPubKey = pickle.loads(recievedPubKey)
            self.sec.load_RSA(properPubKey)
            # then send our public key
            self.TCP_client.sendall(pickle.dumps(self.sec.int_pub_key))
        return None
    

    # this function closes the connection between the two machines
    def _close_connection(self) -> None: 
        self.TCP_client.close()
        self.__regen_UDP()
        self.__regen_TCP()
        self.UDP_binded = False
        return


    # TODO
    # this function sends data to the other machine
    def _send(self, data: any, ignore_errors: bool = False) -> int:
        # if empty raise error
        if data is None and not ignore_errors: raise Exceptions.EmptyDataError()
        # find how many bytes encrypted data is
        encryptedData = self.sec.RSA_encrypt(data)
        intData = int.from_bytes(encryptedData)
        byteCount = intData.bit_length() # how many bits it takes to represent our int
        networkByteOrder = socket.htonl(byteCount)
        self.TCP_client.sendall(pickle.dumps(networkByteOrder)) # send length
        return self.TCP_client.sendall(encryptedData) # send actual data
    

    # TODO
    # temporary recieving function
    def _recv(self) -> None:
        while True:
            # recieve how many bytes message is
            recievedNetworkOrder = self.TCP_client.recv(1024)
            if not recievedNetworkOrder: continue # if empty ("b''")
            unpickledNetworkByteOrder = pickle.loads(recievedNetworkOrder)
            byteCount = socket.ntohl(unpickledNetworkByteOrder)
            # recieve byteCount amount of bytes of data
            while True:
                recievedData = self.TCP_client.recv(byteCount)
                if not recievedData: continue # if empty ("b''") 
                break
            decryptedData = self.sec.RSA_decrypt(recievedData)
            print('recv:', decryptedData)