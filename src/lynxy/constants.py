'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION
'''

# included modules
from enum import Enum

# the main class for containing all of the Enums
# basically fancy constants that keep their color
class Constants:

    # class that contains the constants used
    # generally
    class General(Enum):
        PLACEHOLDER = 'placeholder'


    # class that contains the constants used
    # for config
    class Config(Enum):
        DO_PRINT = 'do print'
        DEFAULT_PORTS = 'default ports'
        IP_OVERRIDE = 'ip override'

    
    # class that contains the constants used
    # for identifying who you are connected to
    class Connection(Enum):
        LYNXY_SERVER = 'lynxy server'
        LYNXY_CLIENT = 'lynxy client'
        GENERAL_SERVER = 'general server'
        GENERAL_CLIENT = 'general client'