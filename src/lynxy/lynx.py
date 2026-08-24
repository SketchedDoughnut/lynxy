'''
This is the main Lynxy file which provides the functions for public use.
A majority of the code is in the comm.py file, and Lynxy just extends the necessary functions.
The rest can be found in the "_comm" class object.
I know this is probably a clunky way to do this but, if it's not broken then don't fix it, right?
'''

# files
from .constants import ConnectionType, ConnectionBias, Event
from .comm import Comm as _Comm
from .pool import Message

####################################################

# the main class for the keeping everything together
class Client:
    '''
    This is the Client class, which creates a Lynxy client object. This allows you to communicate with
    other Lynxy clients and allows you to exchange data between machines.

    Parameters
    ----------
    host: tuple[str, int]
        This is the information for the host machine (that is, your machine) to bind onto, the information being the IP of the host machine and the chosen
        port. The IP should be left empty, as Lynxy will naturally find out the correct IP. However, the port can be set to whatever you
        desire. This information can be acquired with the get_host function.

        ```python
            client = lynxy.Client(('', 50004))
            client.get_host() -> ('192.168.68.x', 50004)
        ```
    '''


    def __init__(self, host: tuple[str, int] = ('', 56774)):
        self._comm = _Comm(host, True)


    # this gets the host information
    def get_host(self) -> tuple[str, int]: 
        '''
        this function gets the IP and port that the host machine is binded to. This is helpful information for the other machine to use for connecting
        the two clients. 

        Returns
        ----------
        tuple[str, int]
            The information of the host, being a pair of the host IP address and port.
        '''
        return self._comm.get_host()


    # this gets the target info
    def get_actual_target(self) -> tuple[str, int]: 
        '''
        when connecting to the other machine, depending on how Lynxy manages things, the other machines port might change when a connection is established.
        You can always check what the current IP and port of the target is by calling this function.

        Returns
        ----------
        tuple[str, int]
            The information of the target machine, being a pair of the target IP address and port.
        '''
        return self._comm.get_actual_target()


    # this function configures heartbeat things for the client
    def config_heartbeat(self, inactive_delay: int = 60, probe_interval: int = 10, probe_count: int = 5) -> None:
        '''
        Lynxy uses heartbeat requests to keep the connection alive, even if no data is sent. 

        Parameters
        ----------
        inactive_delay: int
            This represents how long (in integer seconds) Lynxy should wait before sending heartbeat probe to make sure the other machine
            is alive.
        
        probe_interval: int
            This represents how long (in integer seconds) Lynxy should wait between each heartbeat probe.

        probe_count: int
            This represents how many heartbeat probes Lynxy should send before terminating the connection due to no response. 
            Do note that on Windows machines, the probe_count is decided by the system.
        '''
        self._comm.config_heartbeat(inactive_delay, probe_interval, probe_count)


    # this function sets behaviors for when connection is lost
    def set_connection(self, connection_type: ConnectionType) -> None:
        '''
        The connection type determines what Lynxy will do when a closing event happens. There are three types of connection types.

        Types
        ----------
        ConnectionType.EVENT
            Lynxy will trigger the Event.ON_DISCONNECT event when the connection is closed. This is the default setting.

        ConnectionType.ERROR
            Lynxy will raise the error that occurs on connection closing (graceful or not).

        ConnectionType.NONE
            Lynxy will not do anything when a connection closes.

        Raises
        -----
        TypeError
            If connection_type is not a valid Constants.ConnectionType.
        '''
        # filter out invalid types
        if type(connection_type) != ConnectionType: raise TypeError('Invalid connection type')
        # set connection type
        self._comm.connectionType = connection_type


    # this function starts logging in comm
    # def start_logging(self, debug: bool = False) -> None:
    #     ''' 
    #     This function starts logging in the Lynxy client. Logs are saved to a file named
    #     `lynxy.log`. 

    #     Parameters
    #     ----------
    #     debug: bool
    #         Whether to log when when messages are received / sent. The message itself will not be logged, only its timestamp
    #       and size.
    #     '''
    #     self._comm.start_logging(debug = debug)


    # this function connects to the other machine
    def connect(self, 
                target: tuple[str, int], 
                start_recv: bool = True, 
                timeout: int = 10,
                attempts: int = 6,
                connection_bias: ConnectionBias = ConnectionBias.NONE
    ) -> None: 
        '''
        This function connects client to the other machine, and exchanges encryption keys.

        Parameters
        ----------
        target: tuple[str, int]
            The information of the target machine, the first entry being the IP and the second entry being the port.

        start_recv: bool
            Whether to start the thread for receiving or not. If you want to control when you start receiving, set this to False and call on
          the `lynxy.recv` function when ready to start receiving.

        timeout: int
            How long Lynxy should wait between each attempt to connect to the other client.

        attempts: int
            How many attempts Lynxy should make to connect to the other client.

        connection_bias: ConnectionBias
            Two Lynxy clients will typically find out an order to establish a connection in. They do this by doing a first-second order, where one follows
            the leader. However, if you want one client to always go first, then you can use a connection bias to force that. Do note that the other client does
            not know your connection bias, and will have to be programmed to accomodate the opposite bias. For example,

            ```python
                # case 1
                client 1 -> ConnectionBias.FIRST
                client 2 -> ConnectionBias.LAST

                # case 2
                client 1 -> ConnectionBias.NONE
                client 2 -> ConnectionBias.NONE
            ```
            or vice versa.

        Raises
        ----------
        Exceptions.ConnectionFailedError 
            If handshake or TCP connection fails.
        '''
        self._comm.TCP_connect(
            target_ip = target[0], 
            target_port = target[1], 
            timeout = timeout, 
            attempts = attempts,
            connection_bias = connection_bias
            )
        if start_recv: self.recv()


    # this function closes connections
    def close(self, force: bool = False) -> None: 
        '''
        When called, Lynxy will wait until all data is sent and all data is received before closing.
        
        Parameters
        ----------
        force: bool
            Whether to forcefully close the connection or not.
        '''
        self._comm.close_connection(force)


    # this sends data
    def send(self, data: any, ignore_errors: bool = False, lock_timeout: float = 10.0) -> Message: 
        '''
        When called, Lynxy will send any data you input to the other machine, encrypting it. Data must be pickleable.

        Parameters
        ----------
        data: any
            The data you intend to send, can be anything.

        ignore_errors: bool
            Whether Lynxy should ignore errors and silently return or not. The following errors can be raised if set to False:
          
            ```python
                Lynxy.Exceptions.EmptyDataError() # if sent data is empty
                lynxy.Exceptions.ClientNotConnected() # if client is not connected to other machine
                Lynxy.Exceptions.SendingTimeoutError() # if client can not send after waiting for lock to be released
            ```

            All of these errors are ignored if ignore_errors is set to True.

        lock_timeout: float
            If data is being sent and you try to send more data, Lynxy will wait until the current message is done sending. You can set a timeout that,
            once Lynxy waits up to the timeout amount, a SendingTimeoutError will be raised.

        Returns
        ----------
        Message
            The message object that was sent.
        '''
        return self._comm.send(data, ignore_errors, lock_timeout)


    # this starts receiving data
    def recv(self) -> None:
        '''
        By default, calling the connect function will call this function, which starts receiving data
        in a background thread. However, if you want to control when you start this, then you can set start_recv in `lynxy.Connenct` to False,
        and call this function when your ready.

        ```python
            # you can do this
            client.connect()
            # or this
            client.connect(start_recv = False)
            client.recv() # when you are ready to start receiving
        ```
        '''
        self._comm.start_recv()

    
    # this function sets up decorators for events,
    # basically making integration with comm easier
    def event(self, event: Event):
        '''
        A decorator to add an event to be triggered. Multiple functions can be added to a single event. 

        ```python
            # Example with the ON_MESSAGE event
            @client.event(lynxy.Event.ON_MESSAGE)
            def woohoo_a_function(message: lynxy.Message):
                print(message.content)
        ```

        Parameters
        ----------
        event: Event
            The event to register this function to.
        '''
        # wrapper
        def wrapper(func):
            # make new entry or add to current entry
            if event not in self._comm.eventRegistry.keys():
                self._comm.eventRegistry[event] = [func]
            else:
                self._comm.eventRegistry[event].append(func)
            return func
        return wrapper