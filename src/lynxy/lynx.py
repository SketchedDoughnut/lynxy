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
import socket

# files
from constants import Constants as _Constants
from exceptions import Exceptions as _Exceptions
from secManager import Sec as _Sec

####################################################

# the main class for the connection
class Lynxy:
    def __init__(self):
        '''
        This is a class that represents a handler for connecting
        to any other end you intend to, whether that be another client or a server.
        This class has all the configuration and management for your client instance.
        '''
        ##############
        # # Anything with the value of "Constants.PLACEHOLDER" is that
        # way because it has to be set by the user, or loaded later
        ##############

        # this is an instance of the security manager 
        self.sec = _Sec()

        # this dictionary contains all of the configurable things
        # accessible by the user.
        self.config = {
            _Constants.DO_PRINT: False,
            _Constants.DEFAULT_PORTS: _Constants.PLACEHOLDER
        }
        # this is the IP used for the connection
        self.host = '0.0.0.0'
        # this is the port used for the connection
        self.port = _Constants.PLACEHOLDER
        # this is the client used for sending and recieving
        self.client = None
        # this represents if the client is connected
        self.is_cient_connected = False