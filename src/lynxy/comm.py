'''
This is the comm file, which manages the sockets and communication.
The encryption tools is in the sec.py file, which can be accessed with the "sec" class object. 
The parser tools is in the parser.py file, which can be accessed with the "parser" class object.
'''

# libraries
import threading
import datetime
import platform
import logging
import socket
import random
import pickle
import os

# files
from .exceptions import Exceptions
from .pool import Message, Util
from .parser import Parser
from .constants import *
from .sec import Sec



# this is the main class for the connection
class Comm:
    def __init__(self, host: tuple[str, int] = ['', 56774], UDP_bind: bool = False):
        # this is an instance of the security manager
        self.sec = Sec()
        # this is an instance of the parser
        self.parser = Parser()
        # this is the internal client used for sending and receiving
        if host[0]: self.host = host[0]
        else: self.host = socket.gethostbyname(socket.gethostname())
        self.port = host[1]
        # this is the target info
        self.target = (None, None)
        # this is the actual connected target info (FOR TCP)
        # the difference is that sometimes the information can be different after communicating with the other machine
        self.actual_target = (None, None)
        # this is the client for UDP for finding out who goes first
        self.UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        # this is the main client for communication
        self.TCP_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        # this represents a dictionary of event queues
        self.eventRegistry = {}
        # this represents the connection type for when errors occur
        self.connectionType = ConnectionType.EVENT
        # this is the thread for the receiving function
        self.recvThread = threading.Thread(target=self.recv, daemon=True)
        # this represents the system type
        self.systemType = platform.system()
        # this represents the working directory
        self.wDir = os.path.dirname(os.path.abspath(__file__))
        # this represents if the UDP client is binded or not
        self.UDP_binded = False
        # these are booleans for stopping threads
        self.stopRecv = False
        # this is a lock that, while something is sending, other things can not send
        self.sendLock = threading.Lock()
        # this represents if we have an active connected
        self.connected = False
        # whether to log send/recv calls or not
        self.log_debug = False
        # this dictionary has the different log calls
        self.log_calls = {
            logging.INFO: logging.info,
            logging.CRITICAL: logging.critical,
            logging.DEBUG: logging.debug,
            logging.ERROR: logging.error,
            logging.FATAL: logging.fatal,
            logging.WARNING: logging.warning
        }
        ###########################################################
        # if UDP_bind, immediately bind to host and port
        if UDP_bind: 
            try: self._bind_UDP()
            except OSError: raise Exceptions.AddrAlreadyBindedError()
            self.UDP_binded = True
        ## add default function
        self.eventRegistry[Event.ON_CONN_ATTEMPT] = [self._default_conn_attempt_callback]


    # this is a function to customize logging info requests
    def log(self, logType: int, data: any): 
        if logType == logging.DEBUG and not self.log_debug: return
        self.log_calls[logType](data)


    # default callback for the ON_CONN_ATTEMPT function
    def _default_conn_attempt_callback(self, target: tuple):
        if self.target == target:
            return True
        return False

    
    # this function sets up logging
#     def start_logging(self, debug: bool = False):
#         self.log_debug = debug
#         date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
#         logPath = f'{self.wDir}/_lynxy_{date}.log'
#         # try: os.remove(logPath)
#         # except FileNotFoundError: pass
#         logging.basicConfig(filename=logPath, level=logging.INFO, force=True)
#         message = f'''
# ------------------------------
# Lynxy logging enabled! 
# - host info: {self.host}:{self.port}
# - filename: {__name__}
# - time: {Pool._Tools._format_time()}
# ------------------------------'''
#         self.log(logging.INFO, message)
        

    # this regenerates the UDP client, making a new object
    def _regen_UDP(self) -> None: 
        self.log(logging.INFO, '_regen_UDP: TRY regen UDP')
        self.UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.log(logging.INFO, '_regen_UDP: OK regen UDP')


    # this regenerates the TCP client, making a new object
    def _regen_TCP(self) -> None: 
        self.log(logging.INFO, '_regen_TCP: TRY regen TCP')
        self.TCP_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log(logging.INFO, '_regen_TCP: OK regen TCP')        


    # this binds the UDP client to the host machines ip and port
    def _bind_UDP(self) -> None: 
        self.log(logging.INFO, f'_bind_UDP: TRY bind UDP to {self.host}:{self.port}')
        self.UDP_client.bind((self.host, self.port))
        self.log(logging.INFO, f'_bind_UDP: OK bind UDP to {self.host}:{self.port}')


    # this binds the TCP client to the host machines ip and port
    def _bind_TCP(self) -> None: 
        self.log(logging.INFO, f'_bind_TCP: TRY bind TCP to {self.host}:{self.port}')
        self.TCP_client.bind((self.host, self.port))
        self.log(logging.INFO, f'_bind_TCP: OK bind TCP to {self.host}:{self.port}')


    # this returns the host IP and port in a tuple
    def get_host(self) -> tuple[str, int]: return self.host, self.port


    # this returns the actual target
    # that target being the active TCP connection, not the initial IP and port
    # before connecting
    def get_actual_target(self) -> tuple[str, int]: return self.actual_target
    

    # this starts the recv thread
    # for receiving messages and triggering events
    def start_recv(self) -> None: 
        self.log(logging.INFO, 'start_recv: TRY start recv thread')
        self.TCP_client.settimeout(3.0)
        if not self.recvThread.is_alive(): 
            self.recvThread.start()
            self.log(logging.INFO, 'start_recv: OK start recv thread')
        self.log(logging.INFO, 'start_recv: OK recv thread already started')


    # this function configures heartbeat things for the client
    # such as when to send them, how long to wait between each one, and how many to send
    def config_heartbeat(self, inactive_delay: int = 60, probe_interval: int = 10, probe_count: int = 5) -> None:
        self.log(logging.INFO, 'config_heartbeat: TRY set heartbeat config')
        self.TCP_client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if self.systemType == 'Windows': # Windows-specific options
            keepalive = (1, inactive_delay * 1000, probe_interval * 1000) # On, idle time (ms), interval (ms)
            self.TCP_client.ioctl(socket.SIO_KEEPALIVE_VALS, keepalive)
        elif self.systemType in ('Linux', 'Darwin'): # Linux/macOS-specific options
            self.TCP_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, inactive_delay) # Idle time before sending probes (in seconds)
            self.TCP_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, probe_interval) # Interval between probes (in seconds)
            self.TCP_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, probe_count) # Number of failed probes before closing
        self.log(logging.INFO, 'config_heartbeat: OK set heartbeat config')
        self.log(logging.INFO, f'config_heartbeat:\n     - inactive_delay: {inactive_delay}s\n     - probe_interval: {probe_interval}s\n     -probe_count: {probe_count}')
    

    # this function manages what happens when connection goes wrong,
    # and a connection is closing - typically with an error
    def _handle_close(self, error: BaseException | None = None) -> None:
        # since we know an error happened and the connection likely is 
        # closed, we can force a close 
        self.log(logging.INFO, '_handle_close: TRY force close client')
        # self.log(logging.ERROR, f'_handle_close: error: {error}')
        if self.connected: self.close_connection(force=True)
        self.log(logging.INFO, '_handle_close: OK close client')
        # handle the error according to how client is configured
        self.log(logging.INFO, 'TCP_connect: triggering ON_DISCONNECT/error')
        if self.connectionType == ConnectionType.EVENT: self._dispatch(Event.ON_DISCONNECT, error)
        elif self.connectionType == ConnectionType.ERROR: raise error


    # this function runs the given events when requested
    # events are created using decorators
    def _dispatch(self, eventType: Event, *args) -> list:
        # run every function set up under the event
        res = []
        if eventType not in self.eventRegistry.keys(): return
        for func in self.eventRegistry[eventType]: 
            try: res.append(func(*args))
            except TypeError: raise Exceptions.InvalidFunctionError()
        return res


    # this function handles the UDP connection that helps make the TCP connection
    # as well as the handshake, and the overall connection setup
    def TCP_connect(self, 
                     target_ip: str, 
                     target_port: int, 
                     timeout: int = 10,
                     attempts: int = 6,
                     connection_bias: ConnectionBias = ConnectionBias.NONE
    ) -> bool:
        self.log(logging.INFO, 'TCP_connect: TRY TCP connection')
        # set target machine data
        self.target = (target_ip, target_port)
        self.log(logging.INFO, f'TCP_connect: target machine set to {self.target}')
        # determine whether or not to use UDP
        if connection_bias != ConnectionBias.NONE: 
            # UDP is only used to determine who goes first / second
            # so if we can determine if we are not using it by the connection bias
            first = connection_bias
            self.log(logging.INFO, f'TCP_connect: connection bias set to {connection_bias}')
        else:
            # we use UDP to get the random number
            # if not self.UDP_binded:
            #     self._bind_UDP()
            #     self.UDP_binded = True
            res = self._UDP_connect(timeout, attempts)
            if not res: return False
            ourRandom, targetRandom = res[0], res[1]
            # if True meaning we connect, they recv
            # if False, we recv and they connect
            first = ourRandom > targetRandom
        self.log(logging.INFO, f'TCP_connect: is_first: {first}')
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
        self.log(logging.INFO, 'TCP_connect: OK TCP connection')
        # set up the settings for heartbeat pings
        self.config_heartbeat()
        # do the handshake to exchange RSA keys
        self.log(logging.INFO, 'TCP_connect: TRY handshake')
        self._handshake(first)
        self.log(logging.INFO, 'TCP_connect: OK handshake')
        self.connected = True
        # trigger connect event
        self._dispatch(Event.ON_CONNECT, True)
        self.log(logging.INFO, 'TCP_connect: triggering ON_CONNECT')
        return True


    # this function manages finding out who goes first with making a TCP connection
    # and also who is first with exchanging RSA keys
    def _UDP_connect(self, timeout, attempts) -> tuple[int, int] | None:
        self.log(logging.INFO, 'UDP_connect: TRY UDP connection')
        # first, we bind to our port / ip if not already
        if not self.UDP_binded: 
            # self._regen_UDP()
            self._bind_UDP()
            self.UDP_binded = True
            self.log(logging.INFO, 'UDP_connect: TRY regen, binded')
        # now, we generate and send a random number
        randNum = random.randint(0, 1000) + random.randint(0, 1000)
        self.log(logging.INFO, f'UDP_connect: rand num: {randNum}')
        # we try "attempts" times to connect and wait "timeout" seconds for a response
        connectionSuccess = False
        self.UDP_client.settimeout(timeout)
        for attempt in range(attempts):
            try:
                # if we send the data and get data back,
                # then it succeeded
                try: 
                    self.UDP_client.sendto(str(randNum).encode(), self.target)
                    data, potential_target = self.UDP_client.recvfrom(1024)
                # target machine has not called connect() yet
                except ConnectionResetError: raise Exceptions.TargetUnavailableError()
                # call the callback and see if this target is accepted
                # if not accepted then continue to next attempt
                res = self._dispatch(Event.ON_CONN_ATTEMPT, potential_target)
                if not res[0]: continue
                # accept that target
                self.target = potential_target
                # make sure data got through
                self.UDP_client.sendto(str(randNum).encode(), self.target)
                # we decode the incoming value to make sure the two values aren't equal
                # if they are, we raise error (the chances are very low for this to happen)
                incomingNum = int(data.decode())
                if incomingNum == randNum: raise Exceptions.ConnectionFailedError('Role number generations were equal.')
                # otherwise connection was a success, break
                connectionSuccess = True
                self.log(logging.INFO, f'UDP_connect: received num: {incomingNum}')
                break
            except TimeoutError: 
                self.log(logging.INFO, f'UDP_connect: TIMEOUT {attempt}')
                continue
        # if no success, raise error
        if not connectionSuccess: 
            raise Exceptions.ConnectionFailedError(f'Failed to connect to target machine (UDP) (attempts:{attempts})') 
        self.log(logging.INFO, 'UDP_connect: OK UDP connection')
        # we close our UDP and return the two numbers
        self.UDP_client.close()
        return (randNum, incomingNum)
    

    # this function manages handshakes for exchanging RSA keys
    # which are exchanged just to exchange symmetrical Fernet keys
    def _handshake(self, is_first: bool) -> None:
        self.log(logging.INFO, f'_handshake: first: {is_first}')
        if is_first:
            # we send our public RSA key
            self.TCP_client.sendall(pickle.dumps(self.sec.int_pub_key))
            self.log(logging.INFO, '_handshake: sent public RSA key')
            self.log(logging.INFO, f'_handshake: {self.sec.int_pub_key}')
            # then receive their public RSA key
            receivedPubKey = self.TCP_client.recv(self.sec.keySizeRSA)
            self.sec.load_RSA(pickle.loads(receivedPubKey))
            self.log(logging.INFO, '_handshake: received public RSA key')
            self.log(logging.INFO, f'_handshake: {pickle.loads(receivedPubKey)}')
            # now we send our Fernet key for actual encryption
            # since we are first, we don't need to receive 
            # since the keys are the same
            encryptedFernet = self.sec.RSA_encrypt(self.sec.fernet_key)
            self.TCP_client.sendall(encryptedFernet)
            self.log(logging.INFO, '_handshake: sent Fernet key')
        else:
            # we receive their public key
            receivedPubKey = self.TCP_client.recv(self.sec.keySizeRSA)
            self.sec.load_RSA(pickle.loads(receivedPubKey))
            self.log(logging.INFO, '_handshake: received public RSA key')
            self.log(logging.INFO, f'_handshake: {pickle.loads(receivedPubKey)}')
            # then send our public key
            self.TCP_client.sendall(pickle.dumps(self.sec.int_pub_key))
            self.log(logging.INFO, '_handshake: sent public RSA key')
            self.log(logging.INFO, f'_handshake: {self.sec.int_pub_key}')
            # now we receive the other ends symmetrical token for actual encryption
            # since we are second
            encryptedFernet = self.TCP_client.recv(1024)
            self.sec.load_Fernet(self.sec.RSA_decrypt(encryptedFernet))
            self.log(logging.INFO, '_handshake: received Fernet key')
    

    # this function closes the connection between the two machines
    # gracefully :3
    def close_connection(self, force: bool = False) -> None: 
        self.log(logging.INFO, 'close_connection: TRY close')
        if not self.connected: 
            self.log(logging.INFO, 'close_connection: FAIL close; not connected')
            return
        # if force: self.log(logging.WARNING, 'close_connection: forced closing can cause possible data loss')
        self.stopRecv = True
        self.log(logging.INFO, 'close_connection: TRY stop recv thread')
        if not force: self.recvThread.join()
        else: self.log(logging.INFO, 'close_connection: force bypass stop recv thread')
        self.log(logging.INFO, 'close_connection: OK stop recv thread')
        # this shuts down the read and write pipes gracefully
        # making sure that all data is received and sent properly
        # before closing
        if not force: 
            self.log(logging.INFO, 'close_connection: TRY shutdown client')
            self.TCP_client.shutdown(socket.SHUT_RDWR)
            self.log(logging.INFO, 'close_connection: OK shutdown client')
        self.TCP_client.close()
        self._regen_UDP()
        self._regen_TCP()
        self.UDP_binded = False
        self.connected = False
        self.log(logging.INFO, 'close_connection: OK close')
    

    # this is a function to send data to the other machine
    def send(self, data: any, ignore_errors: bool = False, lock_timeout: float = 10.0) -> Message:
        # raise error message if data is empty and ignore is disabled, or if is none
        # otherwise return
        if data is None and not ignore_errors: raise TypeError('NoneType')
        elif data is None and ignore_errors: return
        elif len(data) == 0 and not ignore_errors: raise Exceptions.EmptyDataError()
        elif len(data) == 0 and ignore_errors: return
        # raise error if not connected
        if not self.connected: 
            if ignore_errors: return
            raise Exceptions.ClientNotConnectedError()
        if not self.sendLock.acquire(timeout=lock_timeout):
            if ignore_errors: return
            raise Exceptions.SendingTimeoutError()
        messageObject = Message(data) # create message object
        encryptedMessage = self.sec.Fernet_encrypt(messageObject) # encrypt data
        paddedMessage = self.parser.addPadding(encryptedMessage) # pad data
        try: 
            self.TCP_client.sendall(paddedMessage) # send actual data
            self.log(logging.DEBUG, f'send: {Util._format_time()} - {len(paddedMessage)} bytes')
        except ConnectionResetError | BrokenPipeError as e: # other machine quit
            self.log(logging.DEBUG, f'send: {Util._format_time()} - {e}')
            self._handle_close(e)
        finally:
            self.sendLock.release()
        return messageObject


    # this is a receiving function for receiving data
    def recv(self) -> None:
        while True:
            if self.stopRecv: return
            try: received = self.TCP_client.recv(1024)
            except TimeoutError as e:
                self.log(logging.DEBUG, f'recv: {Util._format_time()} - {e}')
                continue
            except ConnectionResetError as e: # other machine quit
                self.log(logging.DEBUG, f'recv: {Util._format_time()} - {e}')
                self._handle_close(e)
                return
            except ConnectionAbortedError as e:
                self.log(logging.DEBUG, f'recv: {Util._format_time()} - {e}')
                self._handle_close(e)
                return
            # catch any other error that happens
            # if we are meant to exit thread, just ignore error and exit
            # otherwise raise the same exception again
            except Exception as e:
                self.log(logging.DEBUG, f'recv: {Util._format_time()} - {e}')
                raise e
            # if received is empty, then we got an EOF meaning the other socket
            # shutdown
            if not received: 
                self._handle_close(EOFError('EOF detected: Remote socket shutdown.'))
                return
            # remove padding from the received data
            unpadded = self.parser.removePadding(received)
            self.log(logging.DEBUG, f'recv: {Util._format_time()} - {received} bytes')
            for indiv in unpadded:
                decrypted: Message = self.sec.Fernet_decrypt(indiv)
                decrypted.received_at = Util._format_time()
                self._dispatch(Event.ON_MESSAGE, decrypted)