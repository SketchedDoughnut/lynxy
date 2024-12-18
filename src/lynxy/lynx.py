'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION

Modules included and their uses:
    - socket: for managing connections
    - pickle: for encoding data
    - rsa: for encrypting data

Modules to consider:
    - some multithreading module
    - using cryptography for extra encryption?
'''

# files
from .comm import Comm as _Comm
from .constants import Constants
from .pool import Pool
from .exceptions import Exceptions

# inccluded modules
import threading

####################################################

# the main class for the keeping everything together
class Lynxy:
    def __init__(self, host_ip: str = '', host_port: int = 56774, bind: bool = False):
        '''
        This class keeps everything together with your client and the connection with the other machine.
        It is designed for a TCP communication with the other end.
        This class has all the configuration and management for your client instance. \n
        This class takes 3 arguments:
        - ip: a string of the IP to connect to. This will be set automatically to this machines
              address if not specified.
        - port: an integer of the port to connect to
        - bind: defaulting to False, says whether or not Lynxy should immediately bind to the ip and port. 
                    This is recommended if you want to connect quickly.
        '''
        self._comm = _Comm(host_ip, host_port, bind)
        self._recv_thread = threading.Thread(target=lambda:self._comm._recv(), daemon=True)


    # this gets the host 
    def get_host(self) -> tuple[str, int]: 
        '''
        Gets the information of what IP and port the current host machine is on,
        and returns it in a tuple where the first entry is the IP in a string 
        and the second entry is the port in an integer. For example,
        >>> ('127.0.0.1,', '11111')
        '''
        return self._comm._get_host()


    # this gets the target info
    def get_actual_target(self) -> tuple[str, int]: 
        '''
        Gets the information of what IP and port the target machine is on, and returns it
        in a tuple. Note that the actual port used for communication is different then the one 
        passed into the connect function, but the IP stays the same. Below is an example of a 
        returned tuple:
        >>> ('192.168.68.111', 54454)
        '''
        return self._comm._get_actual_target()


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
    def connect(self, target: tuple[str, int], start_recv: bool = True) -> None: 
        '''
        Connects to the target machine. This function is a shorthand for a variety
        of functions found in _comm. This function has 2 inputs:

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
        '''
        self._comm._TCP_connect(target[0], target[1])
        if start_recv: self.recv()
        return None


    # this function closes connections
    def close(self) -> None: 
        '''
        This closes the connection with the target machine. This does not send a message
        to the target machine, which means that the disconnection will be handled depending
        on how the other machine is configured.
        '''
        self._comm._close_connection()
        return None


    # this sends data
    def send(self, data: any, ignore_errors: bool = False) -> None: 
        '''
        This sends data to the target machine, and only works after connected.
        You are able to send data without recieving data. This function has 2 inputs:

        data: any
        - the data can be any type, and it is encrypted using RSA asymmetrical encryption.
          Everytime you recieve a message, it is in the form of a message object.

        >>> data: Lynxy.Pool.Message

        ignore_errors: bool = True
        - if your data you try to send is empty and this boolean is True, then an error
          will be raised.

        >>> raise Lynxy.Exceptions.EmptyDataError()
        '''
        return self._comm._send(data, ignore_errors)


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
        if not self._recv_thread.is_alive: self._recv_thread.start()
        return None

    
    # this function sets up decorators for events,
    # basically making integration with comm easier
    # TODO 
    # MAKE EVENT FOR DISCONNECTING? GIVE OPTION
    # TO RAISE ERROR INSTEAD
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