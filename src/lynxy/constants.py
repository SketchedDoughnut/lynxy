'''
This is the constants file, which contains all of the constants, either as Enums or literals.
They are used often in function inputs to signifiy different things that are done.
'''

# included modules
from enum import Enum

# the main class for containing all of the Enums
# basically fancy constants that keep their color
class Constants:
    
    # class for all events
    class Event(Enum):
        '''
        This class contains all constants pertaining to events.
        '''
        ON_MESSAGE = 'on message'
        ON_CLOSE = 'on close'
        ON_CONNECT = 'on connect'

    
    # class for all connection types
    class ConnectionType(Enum):
        '''
        This class contains all constants pertaining to different connection types
        '''
        ERROR = 'error'
        EVENT = 'event'
        NONE = 'none'


    # class for all connection biases
    class ConnectionBias:
        '''
        This class contains all constants pertaining to the bias of who goes first when connecting with Lynxy
        '''
        FIRST = True
        LAST = False
        NONE = None