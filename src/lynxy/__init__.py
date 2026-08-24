'''
This is the Lynxy client package, which allows communication with other Lynxy machines.
It simplifies a lot of the things such as security, ease of communication, and more. 
To find documentation, go to the Github~!
- Github: https://github.com/SketchedDoughnut/lynxy
'''

# extending main lynx file
from .lynx import *
from .pool import Message
from .constants import ConnectionType, Event, ConnectionBias
from .exceptions import Exceptions