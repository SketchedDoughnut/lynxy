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
- https://stackoverflow.com/questions/2184181/decoding-tcp-packets-using-python
- https://stackoverflow.com/questions/71547304/python-tcp-socket-is-merging-data

Info about byte order:
- https://www.ibm.com/docs/ja/zvm/7.2?topic=domains-network-byte-order-host-byte-order
- https://stackoverflow.com/questions/71695996/can-you-give-some-practical-uses-of-socket-ntohlx-in-socket-programming-in

Scapy stuff:
- https://scapy.readthedocs.io/en/latest/extending.html#using-scapy-in-your-tools
- https://scapy.readthedocs.io/en/latest/installation.html
- https://scapy.net/

Decorator info:
- https://realpython.com/primer-on-python-decorators/
- https://stackoverflow.com/questions/70982565/how-do-i-make-an-event-listener-with-decorators-in-python

Commenting info:
- https://realpython.com/python-double-underscore/
'''

# included modules
import socket
import random
import pickle

# external modules
from rich import print

# files
from .sec import Sec
from .parser import Parser
from .exceptions import Exceptions
from .constants import Constants

####################################################

# this is the main class for the connection
class Comm:
    def __init__(self, host: str, port: int, UDP_bind: bool):
        # this is an instance of the security manager
        self.sec = Sec()
        # this is an instance of the parser
        self.parser = Parser()
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
        # this represents a dictionary of event queues
        self.eventRegistry = {}
        ###########################################################
        # if UDP_bind, immediately bind to host and port
        if UDP_bind: 
            self.__bind_UDP()
            self.UDP_binded = True


    # this regenerates the UDP client
    def _regen_UDP(self) -> None: self.UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    # this regenerates the TCP client
    def _regen_TCP(self) -> None: self.TCP_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # this binds the UDP client
    def _bind_UDP(self) -> None: self.UDP_client.bind((self.host, self.port))


    # this binds the TCP client
    def _bind_TCP(self) -> None: self.TCP_client.bind((self.host, self.port))


    # this returns the host IP
    def _get_host(self) -> tuple[str, int]: return self.host, self.port


    # this returns the actual target
    # that target being the active TCP connection
    def _get_actual_target(self) -> tuple[str, int]: return self.actual_target
    

    # this function runs the given events
    def _trigger(self, eventType: Constants.Event, data) -> None:
        for func in self.eventRegistry[eventType]: func(data)


    # this function handles the UDP connection that helps make the TCP connection
    def _TCP_connect(self, target_ip: str, target_port: int, timeout: int = 10, attempts: int = 6) -> None:
        # set target machine data
        self.target = (target_ip, target_port)
        # we use UDP to get the random number
        ourRandom, targetRandom = self._UDP_connect(timeout, attempts)
        # we then find out whether to bind our TCP
        # or try to connect to the other end
        self._regen_TCP()
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
                self._regen_TCP()
                self._bind_TCP()
                self.TCP_client.listen(1) # only listen for 1 connection
                self.TCP_client, connectedTarget = self.TCP_client.accept()
                if connectedTarget[0] == self.target[0]: # verify IP, not port
                    self.actual_target = connectedTarget
                    connectionSuccess = True
                    break
            # raise error if connection failed
            if not connectionSuccess: raise Exceptions.ConnectionFailedError(f'Failed to connect to target machine (TCP) (attempts:{attempts})') 
        # do the handshake to exchange RSA keys
        self._handshake(ourRandom > targetRandom)
        return None


    # this function manages finding out who goes first with making a TCP connection
    # and also who is first with exchangin keys
    def _UDP_connect(self, timeout, attempts) -> tuple[int, int]:
        # first, we bind to our port / ip if not already
        if not self.UDP_binded: 
            self._regen_UDP()
            self._bind_UDP()
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

                incomingNum = int(data.decode())
                # otherwise connection was a success, break
                connectionSuccess = True
                break
            except TimeoutError: continue

        # if no success, raise error
        if not connectionSuccess: raise Exceptions.ConnectionFailedError(f'Failed to connect to target machine (UDP) (attempts:{attempts})') 
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
        self._regen_UDP()
        self._regen_TCP()
        self.UDP_binded = False
        return


    # this function sends data to the other machine
    def _send(self, data: any, ignore_errors: bool = False) -> None:
        # raise error message if data is empty
        # and raise is toggled, otherwise return
        raiseError = False
        if len(data) == 0: raiseError = True
        if data is None: raiseError = True
        if not ignore_errors and raiseError: raise Exceptions.EmptyDataError()
        if ignore_errors and raiseError: return
        # find how many bytes encrypted data is
        encryptedData = self.sec.RSA_encrypt(data) # encrypt data
        paddedData = self.parser.addPadding(encryptedData) # pad data
        intData = int.from_bytes(paddedData) # get int of encoded data
        byteCount = intData.bit_length() # how many bits it takes to represent our int
        networkByteOrder = socket.htonl(byteCount) # convert to network (universal) order
        self.TCP_client.sendall(pickle.dumps(networkByteOrder)) # send length
        print('sending:', paddedData)
        self.TCP_client.sendall(paddedData) # send actual data
        return
    

    # TODO
    # temporary recieving function
    def _recv(self) -> None:
        while True:
            # recieve how many bytes message is
            recievedNetworkOrder = self.TCP_client.recv(1024)
            if recievedNetworkOrder is None: continue # if empty ("b''")
            unpickledNetworkByteOrder = pickle.loads(recievedNetworkOrder)
            targetByteCount = socket.ntohl(unpickledNetworkByteOrder)
            # recieve byteCount amount of bytes of data
            # we load leftover to continue where it left off
            recievedData = self.parser.carry

            print('starting with:', recievedData)

            while True:
                recievedData += self.TCP_client.recv(targetByteCount)
                # ensure full data recieved
                intData = int.from_bytes(recievedData)
                recievedByteCount = intData.bit_length()

                print(f'{recievedByteCount}, {targetByteCount}, {recievedData}')

                if recievedByteCount >= targetByteCount: break
            # remove padding
            unpaddedData = self.parser.removePadding(recievedData)
            # decrypt each part
            for indivData in unpaddedData:
                print(f'decrypting ({unpaddedData.index(indivData)}):', indivData)
                decryptedData = self.sec.RSA_decrypt(indivData)
                print(f'recv ({unpaddedData.index(indivData)}):', decryptedData)
                self._trigger(Constants.Event.ON_MESSAGE)