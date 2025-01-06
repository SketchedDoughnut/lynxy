'''
This is the comm file, which manages the sockets and communication.
The encryption tools is in the sec.py file, which can be accessed with the "sec" class object. 
The parser tools is in the parser.py file, which can be accessed with the "parser" class object.
'''

# included modules
import socket
import random
import pickle
import threading
import time
import platform

# files
from .sec import Sec
from .parser import Parser
from .exceptions import Exceptions
from .constants import Constants
from .pool import Pool

####################################################

# TODO ADD LOGGER

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
        # this represents a dictionary of event queues
        self.eventRegistry = {}
        # this represents the connection type for when errors occur
        self.connectionType = Constants.ConnectionType.EVENT
        # this is the thread for the recieving function
        self.recvThread = threading.Thread(target=lambda:self.recv(), daemon=True)
        # this represents the system type
        self.systemType = platform.system()
        # this represents if the UDP client is binded or not
        self.UDP_binded = False
        # these are booleans for stopping threads
        self.stopRecv = False
        # this is a lock that, while something is sending, other things can not send
        self.sendLock = False
        # this represents if we have an active connected
        self.connected = False
        ###########################################################
        # if UDP_bind, immediately bind to host and port
        if UDP_bind: 
            self._bind_UDP()
            self.UDP_binded = True


    # this regenerates the UDP client, making a new object
    def _regen_UDP(self) -> None: self.UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    # this regenerates the TCP client, making a new object
    def _regen_TCP(self) -> None: self.TCP_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # this binds the UDP client to the host machines ip and port
    def _bind_UDP(self) -> None: self.UDP_client.bind((self.host, self.port))


    # this binds the TCP client to the host machines ip and port
    def _bind_TCP(self) -> None: self.TCP_client.bind((self.host, self.port))


    # this returns the host IP and port in a tuple
    def get_host(self) -> tuple[str, int]: return self.host, self.port


    # this returns the actual target
    # that target being the active TCP connection, not the initial IP and port
    # before connectin
    def get_actual_target(self) -> tuple[str, int]: return self.actual_target
    

    # this starts the recv thread
    # for recieving messages and triggering events
    def start_recv(self) -> None: self.recvThread.start() if not self.recvThread.is_alive() else None


    # this function configures heartbeat things for the client
    # such as when to send them, how long to wait between each one, and how many to send
    def config_heartbeat(self, inactive_delay: int = 60, probe_interval: int = 10, probe_count: int = 5) -> None:
        self.TCP_client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if self.systemType == 'Windows': # Windows-specific options
            keepalive = (1, inactive_delay * 1000, probe_interval * 1000) # On, idle time (ms), interval (ms)
            self.TCP_client.ioctl(socket.SIO_KEEPALIVE_VALS, keepalive)
        elif self.systemType in ('Linux', 'Darwin'): # Linux/macOS-specific options
            self.TCP_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, inactive_delay) # Idle time before sending probes (in seconds)
            self.TCP_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, probe_interval) # Interval between probes (in seconds)
            self.TCP_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, probe_count) # Number of failed probes before closing
    

    # this function manages what happens when connection goes wrong,
    # and a connection is closing - typically with an error
    def _handle_close(self, error: Exception | None = None) -> None:
        # since we know an error happened and the connection likely is 
        # closed, we can force a close 
        if self.connected: self.close_connection(force=True)
        # handle the error according to how client is configured
        if self.connectionType == Constants.ConnectionType.EVENT: self._trigger(Constants.Event.ON_CLOSE, error)
        elif self.connectionType == Constants.ConnectionType.ERROR: raise error


    # this function runs the given events when requested
    # events are created using decorators
    def _trigger(self, eventType: Constants.Event, data) -> None:
        # run every function set up under the event
        try:
            for func in self.eventRegistry[eventType]: 
                func(data)
        # if no functions then there will be a key error, this is fine
        # so we can ignore
        except KeyError: return


    # this function handles the UDP connection that helps make the TCP connection
    # as well as the handshake, and the overall connection setup
    def TCP_connect(self, 
                     target_ip: str, 
                     target_port: int, 
                     timeout: int = 10,
                     attempts: int = 6,
                     connection_bias: Constants.ConnectionBias = Constants.ConnectionBias.NONE
                     ) -> None:
        # set target machine data
        self.target = (target_ip, target_port)
        # determine whether or not to use UDP
        if connection_bias != Constants.ConnectionBias.NONE: 
            # UDP is only used to determine who goes first / second
            # so if we can determine if we are not using it by the connection bias
            first = connection_bias
        else:
            # we use UDP to get the random number
            ourRandom, targetRandom = self._UDP_connect(timeout, attempts)
            # if True meaning we connect, they recv
            # if False, we recv and they connect
            first = ourRandom > targetRandom
        # we then find out whether to bind our TCP
        # or try to connect to the other end
        self._regen_TCP()
        if first:
            self.TCP_client.connect(self.target)
            self.actual_target = self.target
        else:
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
        # set up the settings for heartbeat pings
        self.config_heartbeat()
        # do the handshake to exchange RSA keys
        self._handshake(first)
        self.connected = True
        # trigger connect event
        self._trigger(Constants.Event.ON_CONNECT, True)


    # this function manages finding out who goes first with making a TCP connection
    # and also who is first with exchanging RSA keys
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
        # we close our UDP and return the two numbers
        self.UDP_client.close()
        return (randNum, incomingNum)
    

    # this function manages handshakes for exchanging RSA keys
    # which are exchanged just to exchange symmetrical Fernet keys
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
    

    # this function closes the connection between the two machines
    # gracefully :3
    def close_connection(self, force: bool = False) -> None: 
        if not self.connected: return
        self.stopRecv = True
        # this shuts down the read and write pipes gracefully
        # making sure that all data is recieved and sent properly
        # before closing
        if not force: self.TCP_client.shutdown(socket.SHUT_RDWR)
        self.TCP_client.close()
        self._regen_UDP()
        self._regen_TCP()
        self.UDP_binded = False
        self.connected = False
    

    # this is a function to send data to the other machine
    def send(self, data: any, ignore_errors: bool = False, lock_timeout: float = 10.0) -> None:
        # raise error message if data is empty and ignore is disabled,
        # otherwise return
        if len(data) == 0 or data is None:
            if ignore_errors: return
            raise Exceptions.EmptyDataError()
        # raise error if not connected
        if not self.connected: 
            if ignore_errors: return
            raise Exceptions.ClientNotConnectedError()
        # wait until no longer a lock on sending or if we reach the lock timeout
        timeout = time.time() + lock_timeout
        while self.sendLock:
            if time.time() >= timeout:
                if ignore_errors: return
                raise Exceptions.SendingTimeoutError()
        # set the send lock to True so that any other calls to send
        # data have to wait to send their data
        self.sendLock = True
        messageObject = Pool.Message(data) # create message object
        encryptedMessage = self.sec.Fernet_encrypt(messageObject) # encrypt data
        paddedMessage = self.parser.addPadding(encryptedMessage) # pad data
        try: 
            self.TCP_client.sendall(paddedMessage) # send actual data
            self.sendLock = False
        except ConnectionResetError as e: # other machine quit
            self.sendLock = False
            self._handle_close(e)
        except BrokenPipeError as e: # connection was properly closed and sending data was attempted
            self.sendLock = False
            self._handle_close(e)


    # this is a recieving function for recieving data
    def recv(self) -> None:
        while True:
            try: recieved = self.TCP_client.recv(1024)
            except ConnectionResetError as e: # other machine quit
                self._handle_close(e)
                return
            except ConnectionAbortedError as e: # host client closed
                self._handle_close(e)
                return
            # catch any other error that happens
            # if we are meant to exit thread, just ignore error and exit
            # otherwise raise the same exception again
            except Exception as e:
                if self.stopRecv: return
                raise e
            # if recieved is empty, then we got an EOF meaning the other socket
            # shutdown
            if not recieved: 
                self._handle_close(EOFError('EOF detected: Remote socket shutdown.'))
                return
            # remove padding from the recieved data
            unpadded = self.parser.removePadding(recieved)
            for indiv in unpadded:
                decrypted: Pool.Message = self.sec.Fernet_decrypt(indiv)
                decrypted.recieved_at = Pool._Tools._format_time()
                self._trigger(Constants.Event.ON_MESSAGE, decrypted)