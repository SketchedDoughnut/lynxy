'''
This is the main Lynxy file which provides the functions for public use.
A majority of the code is in the comm.py file, and Lynxy just extends the necessary functions.
The rest can be found in the "_comm" class object.
I know this is probably a clunky way to do this but, if it's not broken then don't fix it, right?
'''

# files
from .comm import Comm as _Comm
from .constants import Constants
from .pool import Pool
from .exceptions import Exceptions

####################################################

# the main class for the keeping everything together
class Lynxy:
    def __init__(self, host: tuple[str, int] = ['', 56774], bind: bool = False):
        '''
        This is the Lynxy class, which creates a Lynxy client object. This allows you to communicate with
        other Lynxy clients and allows you to exchange data between machines. More specifics about certain functionalities
        can be found on the official documentation on Github!

        host: tuple[str, int] = ['', 56774]
        - this is the information for the host machine to bind onto, the information being the IP of the host machine and the chosen
          port. The IP should be left empty, as Lynxy will naturally find out the correct IP. However, the port can be set to whatever you
          desire. This information can be acquired with the get_host function

          >>> client = Lynxy(['', 50004])
          >>> client.get_host() -> ['192.168.68.x', 50004]

        bind: bool = False
        - this decides whether or not you immediately bind to the host IP and port, or if you want to wait until you call the connect function.
        '''
        self._comm = _Comm(host, bind)


    # this gets the host information
    def get_host(self) -> tuple[str, int]: 
        '''
        this function gets the IP and port that the host machine is binded to. This is helpful information for the other machine to use for connecting
        the two clients. 

        The first entry in the tuple is the IP, and the second entry is the port.
        '''
        return self._comm.get_host()


    # this gets the target info
    def get_actual_target(self) -> tuple[str, int]: 
        '''
        when connecting to the other machine, depending on how Lynxy manages things, the other machines port might change when a connection is established.
        You can always check what the current IP and port of the target is by calling this function, which returns a tuple where the first entry is the IP,
        and the second entry is the port.
        '''
        return self._comm.get_actual_target()


    # this function configures heartbeat things for the client
    def config_heartbeat(self, inactive_delay: int = 60, probe_interval: int = 10, probe_count: int = 5) -> None:
        '''
        Lynxy uses heartbeat requests to keep the connection alive, even if no data is sent. 

        inactive_delay: int = 60
        - this represents how long (in integer seconds) Lynxy should wait before sending heartbeat probe to make sure the other machine
            is alive.
        
        probe_interval: int = 10
        - this represents how long (in integer seconds) Lynxy should wait between each heartbeat probe.

        probe_count: int = 5
        - this represents how many heartbeat probes Lynxy should send before terminating the connection due to no response. 

        Do note that on Windows machines, the probe_count is decided by the system.
        '''
        self._comm.config_heartbeat(inactive_delay, probe_interval, probe_count)


    # this function sets behaviors for when connection is lost
    def set_connection(self, connectionType: Constants.ConnectionType) -> None:
        '''
        The connection type determines what Lynxy will do when a closing event happens. There are three types of connection types.

        ConnectionType.EVENT
        - Lynxy will trigger the Event.ON_CLOSE event when the connection is closed. This is the default setting.

        ConnectionType.ERROR
        - Lynxy will raise the error that occurs on connection closing (graceful or not).

        ConnectionType.NONE
        - Lynxy will not do anything when a connection closes.
        '''
        # filter out invalid types
        if type(connectionType) != Constants.ConnectionType: raise TypeError('Invalid connection type')
        # set connection type
        self._comm.connectionType = connectionType
        return None


    # this function connects to the other machine
    def connect(self, 
                target: tuple[str, int], 
                start_recv: bool = True, 
                timeout: int = 10,
                attempts: int = 6,
                connection_bias: Constants.ConnectionBias = Constants.ConnectionBias.NONE
                ) -> None: 
        '''
        This function connects client to the other machine, and exchanges some data to keep things secure.

        target: tuple[str, int]
        - the information of the target machine, the first entry being the IP and the second entry being the port.

        start_recv: bool = True
        - whether to start the thread for recieving or not. If you want to control when you start recieving, set this to False and call on
          the recv function when ready.

        timeout: int = 10
        - how long Lynxy should wait on each attempt to connect to the other client.

        attempts: int = 6
        - how many attempts Lynxy should make to connect to the other client.

        connection_bias: Constants.ConnectionBias = Constants.ConnectionBias.NONE
        - two Lynxy clients will typically find out an order to establish a connection in. They do this by doing a first-second order, where one follows
          the leader. However, if you want one client to always go first, then you can use a connection bias to force that. Do note that the other client does
          not know your connection bias, and will have to be programmed to accomodate the opposite bias. For example,

          >>> # client 1 has a bias of first
          >>> # client 2 has to have a bias of second
          >>> # or vice versa
        '''
        self._comm.TCP_connect(
            target_ip = target[0], 
            target_port = target[1], 
            timeout = timeout, 
            attempts = attempts,
            connection_bias = connection_bias
            )
        if start_recv: self.recv()
        return None


    # this function closes connections
    def close(self, force: bool = False) -> None: 
        '''
        When called, Lynxy will wait until all data is sent and all data is recieved before closing.
        However, if you set force to True, Lynxy will immediately terminate the connection. This can result in 
        data being lost.
        '''
        self._comm.close_connection(force)
        return None


    # this sends data
    def send(self, data: any, ignore_errors: bool = False, lock_timeout: float = 10.0) -> None: 
        '''
        When called, Lynxy will send any data you input to the other machine, encrypting it.

        data: any
        - the data you intend to send, can be anything.

        ignore_errors: bool = False
        - whether Lynxy should ignore errors and silently return or not. The following errors can be raised if set to False:
          
          >>> Lynxy.Exceptions.EmptyDataError() # if sent data is empty
          >>> lynxy.Exceptions.ClientNotConnected() # if client is not connected to other machine
          >>> Lynxy.Exceptions.SendingTimeoutError() # if client can not send after waiting for lock to be released

          All of these errors are ignored if ignore_errors is set to True.

        lock_timeout: float = 10.0
        - if data is being sent and you try to send more data, Lynxy will wait until the current message is done sending. You can set a timeout that,
          once Lynxy waits up to the timeout amount, a SendingTimeoutError will be raised.

        '''
        return self._comm.send(data, ignore_errors, lock_timeout)


    # this starts recieving data
    def recv(self) -> None:
        '''
        By default, calling the connect function will call this function, which starts recieving data
        in a background thread. However, if you want to control when you start this, then you can set start_recv in connect to False,
        and call this function when your ready.

        >>> # do this
        >>> client.connect()
        >>> # or
        >>> client.connect(start_recv = False)
        >>> client.recv() # when you're ready to start recieving
        '''
        self._comm.start_recv()
        return None

    
    # this function sets up decorators for events,
    # basically making integration with comm easier
    def event(self, eventType: Constants.Event):
        '''
        Lynxy has different events that they trigger when things happen. For example, every time a message is recieved, Lynxy will
        trigger the message event. Events can be set up as a decorators, and each event passes in different data into your function.
        Below is an example with the ON_MESSAGE event.

        >>> @client.event(lynxy.Constants.Event.ON_MESSAGE)
        >>> def woo_hoo_a_function(message: lynxy.Pool.Message):
        >>>     print(message.content)
        '''
        # wrapper function that is returned,
        # i am not quite sure how this works but it wraps around
        # the inputted function?
        def wrapper(func):
            # make a new entry for this event if it doesn't exist
            # this function will be ran everytime the event is triggered
            if eventType not in self._comm.eventRegistry.keys(): 
                self._comm.eventRegistry[eventType] = [func]
            # append function
            else: self._comm.eventRegistry[eventType].append(func)
        return wrapper