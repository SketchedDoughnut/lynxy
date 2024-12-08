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

# included modules
import os

# files
from .constants import Constants
from .exceptions import Exceptions
from .comm import Comm

####################################################

# the main class for the keeping everything together
class Lynxy:
    def __init__(self, ip: str = '', port: int = 56774, UDP_bind: bool = False):
        '''
        This class keeps everything together with your client and the connection with the other machine.
        It is designed for a TCP communication with the other end.
        This class has all the configuration and management for your client instance. \n
        This class takes 3 arguments:
        - ip: a string of the IP to connect to
        - port: an integer of the port to connect to
        - UDP_bind: defaulting to False, says whether or not Lynxy should immediately bind to the ip and port. 
                    This is recommended if you want to connect quickly.
        '''
        # this is the current working directory
        self.wDir = os.path.dirname(os.path.abspath(__file__))
        # this decides certain configurable stuff
        self.config = {
            Constants.Config.DO_PRINT: False
        }
        # this is the manager for communications
        self.comm = Comm(ip, port, UDP_bind)


    # this function connects to the other machine
    def connect(self, ip, port) -> None: self.comm.TCP_connect(ip, port)


    # a function used to distinguish whether or not to print,
    # different from the default printing function but not overwriting it
    def pprint(self, data: str) -> None: print(data) if self.do_print else print('', end='')