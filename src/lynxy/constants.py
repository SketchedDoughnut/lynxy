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
        ON_MESSAGE = 'on_message'