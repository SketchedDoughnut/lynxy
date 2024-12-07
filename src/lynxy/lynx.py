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
import pickle

# external modules
import rsa

# files
from constants import Constants

####################################################
# STATIC VARS (not accessing files or other dynamic loading)

# this dictionary contains all of the configurable things
# accessible by the user.
# Anything with the value of "Constants.PLACEHOLDER" is that
# way because it has to be set by the user, or loaded later
_config = {
    Constants.DO_PRINT: False,
    Constants.DEFAULT_PORTS: Constants.PLACEHOLDER
}

