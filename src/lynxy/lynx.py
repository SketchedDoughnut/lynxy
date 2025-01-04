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
        TODO WRITE DOCUMENTATION
        '''
        self._comm = _Comm(host, bind)


    # this gets the host information
    def get_host(self) -> tuple[str, int]: 
        '''
        TODO WRITE DOCUMENTATION
        '''
        return self._comm.get_host()


    # this gets the target info
    def get_actual_target(self) -> tuple[str, int]: 
        '''
        TODO WRITE DOCUMENTATION
        '''
        return self._comm.get_actual_target()


    # this function sets behaviors for when connection is lost
    def set_connection(self, connectionType: Constants.ConnectionType) -> None:
        '''
        TODO WRITE DOCUMENTATION
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
        TODO WRITE DOCUMENTATION
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
        TODO WRITE DOCUMENTATION
        '''
        self._comm.close_connection(force)
        return None


    # this sends data
    def send(self, data: any, ignore_errors: bool = False, lock_timeout: float = 10.0) -> None: 
        '''
        TODO WRITE DOCUMENTATION
        '''
        return self._comm.send(data, ignore_errors, lock_timeout)


    # this starts recieving data
    def recv(self) -> None:
        '''
        TODO WRITE DOCUMENTATION
        '''
        self._comm.start_recv()
        return None

    
    # this function sets up decorators for events,
    # basically making integration with comm easier
    def event(self, eventType: Constants.Event):
        '''
        TODO 
        WRITE DOCUMENTATION
        TALK ABOUT THE DIFFERENT TYPES OF DATA FOR DIFFERENT EVENTS
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