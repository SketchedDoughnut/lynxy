'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION
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
        ON_CLOSE ='on close'

    
    # class for all connection types
    class ConnectionType(Enum):
        '''
        This class contains all conatins pertaining to different connection types
        '''
        ERROR = 'error'
        EVENT = 'event'