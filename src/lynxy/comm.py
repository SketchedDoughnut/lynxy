'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION
'''

# included modules
import socket
import random
import pickle
import threading

# files
from .sec import Sec
from .parser import Parser
from .exceptions import Exceptions
from .constants import Constants
from .pool import Pool

####################################################

# this is the main class for the connection
class Comm:
    def __init__(self, host: tuple[str, int] = ['', 56774], UDP_bind: bool = False):
        # this is an instance of the security manager
        self.sec = Sec()
        # this is an instance of the parser
        self.parser = Parser()
        # this is the internal client used for sending and recieving
        if host[0]: self.host = host[0]
        else: self.host = socket.gethostbyname(socket.gethostname())
        self.port = host[1]
        # this is the target info
        self.target = (None, None)
        # this is the actual connected target info (FOR TCP)
        self.actual_target = (None, None)
        # this is the client for UDP for finding out who goes first
        self.UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        # this is the main client for communication
        self.TCP_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        # this represents if the UDP client is binded or not
        self.UDP_binded = False
        # this represents a dictionary of event queues
        self.eventRegistry = {}
        # this represents the connection type for when errors occur
        self.connectionType = Constants.ConnectionType.EVENT
        # this is the thread for the recieving function
        self.recvThread = threading.Thread(target=lambda:self.recv(), daemon=True)
        # this represents a var for stopping thread
        self.stopThread = False
        # this represents if we have an active connected
        self.connected = False
        ###########################################################
        # if UDP_bind, immediately bind to host and port
        if UDP_bind: 
            self._bind_UDP()
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
    def get_host(self) -> tuple[str, int]: return self.host, self.port


    # this returns the actual target
    # that target being the active TCP connection
    def get_actual_target(self) -> tuple[str, int]: return self.actual_target
    

    # this starts the recv thread
    def start_recv(self) -> None: self.recvThread.start() if self.recvThread.is_alive() else None


    # this function manages what happens when connection goes wrong
    def _connection_error(self, error: Exception | None = None) -> None:
        if self.connected:
            self.close_connection()
            self.connected = False
        if self.connectionType == Constants.ConnectionType.EVENT:
            self._trigger(Constants.Event.ON_CLOSE, error)
        elif self.connectionType == Constants.ConnectionType.ERROR: 
            raise error
        return None


    # this function runs the given events
    def _trigger(self, eventType: Constants.Event, data) -> None:
        # run every function set up under the event
        try:
            for func in self.eventRegistry[eventType]: 
                func(data)
        # if no functions then ther will be a key error, this is fine
        # so we can ignore
        except KeyError: return


    # this function handles the UDP connection that helps make the TCP connection
    def TCP_connect(self, 
                     target_ip: str, 
                     target_port: int, 
                     timeout: int = 10,
                     attempts: int = 6
                     ) -> None:
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
        self.connected = True
        self._trigger(Constants.Event.ON_CONNECT, True)
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
                # we decode the incoming value to make sure the two values aren't equal
                # if they are, we raise error (the chances are very low for this to happen)
                incomingNum = int(data.decode())
                if incomingNum == randNum: raise Exceptions.ConnectionFailedError('Role number generations were equal.')
                # otherwise connection was a success, break
                connectionSuccess = True
                break
            except TimeoutError: continue
        # if no success, raise error
        if not connectionSuccess: 
            raise Exceptions.ConnectionFailedError(f'Failed to connect to target machine (UDP) (attempts:{attempts})') 
        # we close our UDP and return
        self.UDP_client.close()
        return (randNum, incomingNum)
    

    # this function manages handshakes
    def _handshake(self, is_first: bool) -> None:
        if is_first:
            # we send our public RSA key
            self.TCP_client.sendall(pickle.dumps(self.sec.int_pub_key))
            # then recieve their public RSA key
            recievedPubKey = self.TCP_client.recv(1024)
            self.sec.load_RSA(pickle.loads(recievedPubKey))
            # now we send our Fernet key for actual encryption
            # since we are first, we don't need to recieve 
            # since the keys are the same
            encryptedFernet = self.sec.RSA_encrypt(self.sec.fernet_key)
            self.TCP_client.sendall(encryptedFernet)
        else:
            # we recieve their public key
            recievedPubKey = self.TCP_client.recv(1024)
            self.sec.load_RSA(pickle.loads(recievedPubKey))
            # then send our public key
            self.TCP_client.sendall(pickle.dumps(self.sec.int_pub_key))
            # now we recieve the other ends symmetrical token for actual encryption
            # since we are second
            encryptedFernet = self.TCP_client.recv(1024)
            self.sec.load_Fernet(self.sec.RSA_decrypt(encryptedFernet))
        return None
    

    # this function closes the connection between the two machines
    # TODO
    # implement system to signify other end that is closing?
    def close_connection(self) -> None: 
        self.stopThread = True
        self.TCP_client.close()
        self._regen_UDP()
        self._regen_TCP()
        self.UDP_binded = False
        return None
    

    # this is a function to send data to the other end
    def send(self, data: any, ignore_errors: bool = False) -> None:
        # raise error message if data is empty and ignore is disabled,
        # otherwise return
        raiseError = False
        if len(data) == 0: raiseError = True
        if data is None: raiseError = True
        if not ignore_errors and raiseError: raise Exceptions.EmptyDataError()
        if ignore_errors and raiseError: return
        messageObject = Pool.Message(data) # create message object
        if not self.connected: raise Exceptions.ClientNotConnectedError()
        encryptedMessage = self.sec.Fernet_encrypt(messageObject) # encrypt data
        paddedMessage = self.parser.addPadding(encryptedMessage) # pad data
        try: self.TCP_client.sendall(paddedMessage) # send actual data
        except ConnectionResetError as e: self._connection_error(e) # other end quit
        return None


    # this is a recieving function for recieving data
    # TODO 
    # fix error handling, its way too vague right now and isn't coded well
    def recv(self) -> None:
        while True:
            try: recieved = self.TCP_client.recv(1024)
            except ConnectionResetError as e: # other end quit
                self._connection_error(e)
                return
            except ConnectionAbortedError as e: # this end quit and thread is running
                self._connection_error(e)
                return
            except: 
                if self.stopThread: return # stop regardless if wanted
            unpadded = self.parser.removePadding(recieved)
            for indiv in unpadded:
                decrypted: Pool.Message = self.sec.Fernet_decrypt(indiv)
                decrypted.recieved_at = Pool._Tools._format_time()
                self._trigger(Constants.Event.ON_MESSAGE, decrypted)