'''
FOR ANYONE LOOKING AT THE SOURCE CODE:

This is the main Lynxy file which provides the functions used by people.
A majority of the code is in comm.py, and Lynxy sometimes just does a little logic before
passing on function inputs to the ones further down in comm. I am not sure why I made it this way,
but it looks nice and works well so if it works don't fix it, right?
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
        This class creates an instance of Lynxy for use with communication with the other machine.
        It is designed for usage with a TCP connection.

        ## Arguments
        host: tuple[str, int] = ['', 56774]
        - the host information of this machine to bind to. If the IP is left empty, it will automatically be set to the proper IP.
          the binded information can be acquired with the function get_host().

        bind: bool = False
        - Says whether or not Lynxy should immediately bind to the given IP and port. This is recommended if you want to connect quickly.
        '''
        self._comm = _Comm(host, bind)


    # this gets the host information
    def get_host(self) -> tuple[str, int]: 
        '''
        Gets the information of what IP and port the current host machine is on,
        and returns it in a tuple. Below is an example:

        >>> ('019.78.654.321,', '11111')

        If the client has not binded, then this will return a tuple of (None, None).
        '''
        return self._comm.get_host()


    # this gets the target info
    def get_actual_target(self) -> tuple[str, int]: 
        '''
        Gets the information of what IP and port the target machine is on, and returns it
        in a tuple. Note that the actual port used for communication is different then the one 
        passed into the connect function, but the IP stays the same. Below is an example of a 
        returned tuple:

        >>> ('123.456.78.910', 54454)

        If the client has not connected, then this will return a tuple of (None, None).
        '''
        return self._comm.get_actual_target()


    # this function sets behaviors for when connection is lost
    def set_connection(self, connectionType: Constants.ConnectionType) -> None:
        '''
        Sets the connection type. This is used to determine what to do after 
        the other machine stops communicating. Information about the individual
        information types can be found on the Github documentation. (TODO)
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
                attempts: int = 6
                ) -> None: 
        '''
        Connects to the target machine. This function is a shorthand for a variety
        of functions found in _comm.

        When Lynxy tries to connect to another client, it first uses UDP to determine which client will
        be first and second (for simplifying connecting). Next, it uses TCP for the actual
        connection, exchanging some initial data such as encryption keys. For this reason,
        Lynxy can raise errors either when attempting the UDP connection, or afterwards
        when attempting to form a TCP connection.

        This function has 4 arguments:

        target: tuple[str, int]
        - a tuple of the target machines IP as a string, and the target machines
          port as an integer.
        
        start_recv: bool = True
        - a boolean used for starting the thread for recieving data. This justs
          calls on the function recv(). Set this to False if you want to choose
          when to start recieving data yourself by calling recv()

        >>> # create my client instance,
            inst = Lynxy()
            # connect to the other machine and automatically start recieving,
            inst.connect()

        Or if you want to manually choose when to recieve,

        >>> inst.connect(start_recv = False)
            # when you want to start,
            inst.recv()

        timeout: int = 10
        - when attempting to connect, the timeout is used to determine how long to wait before the 
          connection fails, and it should try again. It will try (attempts) amount of times to connect.

        attempts: int = 6
        - when attempting to connect, lynxy will try (attempts) times. An attempt fails after (timeout) seconds passes.
          If Lynxy fails to form a UDP / TCP connection after all attempts fail, then it will raise the following error:

          >>> Lynxy.Exceptions.ConnectionFailedError(f'Failed to connect to target machine ((UDP/TCP)) (attempts:{attempts})') 

        '''
        self._comm.TCP_connect(
            target_ip = target[0], 
            target_port = target[1], 
            timeout = timeout, 
            attempts = attempts
            )
        if start_recv: self.recv()
        return None


    # this function closes connections
    def close(self) -> None: 
        '''
        This closes the connection with the target machine.
        '''
        self._comm.close_connection()
        return None


    # this sends data
    def send(self, data: any, ignore_errors: bool = False) -> None: 
        '''
        This sends data to the target machine, and only works after connected.
        You are able to send data without recieving data. 
        
        This function has 2 arguments:

        data: any
        - the data can be any type, and it is encrypted using AES Fernet encryption.
          Everytime you recieve a message, it is in the form of a message object:

        >>> Lynxy.Pool.Message

        ignore_errors: bool = True
        - if your data you try to send is empty and this boolean is True, then the following error
        will be raised:

        >>> Lynxy.Exceptions.EmptyDataError()
        '''
        return self._comm.send(data, ignore_errors)


    # this starts recieving data
    def recv(self) -> None:
        '''
        This function starts the thread that recieves data from the target machine.
        This will not start the thread if it is already running, and if you run connect
        with start_recv as True, this will be ran for you.

        >>> connect(start_recv = True)
            # or
            connect(start_recv = False)
            recv()
        '''
        self._comm.start_recv()
        return None

    
    # this function sets up decorators for events,
    # basically making integration with comm easier
    def event(self, eventType: Constants.Event):
        '''
        This function is made to be used as a decorator for different events.
        These events can be found at:

        >>> lynxy.Constants.Event

        Every time the given event is triggered, the function that you provide
        below the event will be ran. Each event has data that it will pass in to your function.
        More information about data types can be found in the documentation on Github. (TODO)

        Below is an working example of something you might do:

        >>> inst = lynxy.Lynxy()
            @inst.event(lynxy.Constants.Event.ON_MESSAGE)
            def do_stuff(data: lynxy.Pool.Message):
                print('stuff is done!')
        '''
        # wrapper function that is returned,
        # i am not quite sure how this works but it wraps around
        # the inputted function?
        def wrapper(func):
            # make a new entry for this event if it doesn't exist
            if eventType not in self._comm.eventRegistry.keys(): 
                self._comm.eventRegistry[eventType] = [func]
            # append function
            else: self._comm.eventRegistry[eventType].append(func)
        return wrapper