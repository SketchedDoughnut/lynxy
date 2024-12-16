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
        # this decides certain configurable stuff
        # self.config = {
        #     Constants.Config.DO_PRINT: False
        # }
        # this is the manager for communications
        self._comm = _Comm(host_ip, host_port, bind)


    # this function connects to the other machine
    def connect(self, target_ip, target_port) -> None: self._comm._TCP_connect(target_ip, target_port)


    # this function closes connections
    def close(self) -> None: self._comm._close_connection()


    # this gets the host 
    def get_host(self) -> tuple[str, int]: return self.comm._get_host()


    # this gets the target info
    def get_actual_target(self) -> tuple[str, int]: return self._comm._get_actual_target()


    # this sends data
    def send(self, data: any, ignore_errors: bool = False) -> None: return self._comm._send(data, ignore_errors)

    
    # this function sets up decorators for events,
    # basically making integration with comm easier
    def event(self, eventType: Constants.Event):
        # wrapper function that is returned,
        # i am not quite sure how this works but it wraps around
        # the inputted function?
        def wrapper(func): 
            # make a new entry for this event if it doesn't exist
            if eventType not in self._comm.eventRegistry.keys(): 
                self._comm.eventRegistry[eventType] = [func]
            else: self._comm.eventRegistry[eventType].append(func)
        return wrapper