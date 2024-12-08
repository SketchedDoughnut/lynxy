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
import os
import json

# files
from constants import Constants
from exceptions import Exceptions
from sec import Sec

####################################################

# the main class for the connection
class Lynxy:
    def __init__(self):
        '''
        This is a class that represents a handler for connecting
        to any other end you intend to, whether that be another client, server, or lynxy server.
        This class has all the configuration and management for your client instance.
        '''
        ##############
        # # Anything with the value of "Constants.General.PLACEHOLDER" is that
        # way because it has to be set by the user, or loaded later
        ##############
        # this is the current working directory
        self.wDir = os.path.dirname(os.path.abspath(__file__))
        # this is an instance of the security manager 
        self.sec = Sec()
        # this dictionary contains all of the configurable things
        # accessible by the user.
        self.config = {
            Constants.Config.DO_PRINT: False,
            Constants.Config.DEFAULT_PORTS: Constants.General.PLACEHOLDER,
            Constants.Config.IP_OVERRIDE: None
        }
        # this is the IP used for the connection
        self.host = ''
        # this is the port used for the connection
        self.port = Constants.General.PLACEHOLDER
        # this is the client used for sending and recieving
        self.client = None
        # this represents if the client is connected
        self.is_cient_connected = False


    # a function to load the default ports from a file
    # def load_default_ports(self):
        

    # a function for setting the externally configurable data
    def set_config(self, ID: Constants.Config, data: any, save_ports: bool = False) -> None:
        '''
        This is a function that allows you to configure certain internal values.
        - ID: is used as a key in a dictionary to find out what data to change.
              The ID is from lynxy.Constants.Config, and should match with the data you
              are inputting. For example, if ID is lynxy.Constants.Config.DEFAULT_PORTS, 
              then data should be a list of integer ports.
        - data: is used for changing the actual data in the config dictionary. As 
                previously mentioned, your data type must match up with the inputted
                ID.
        - save_ports: is used if ID is lynxy.Constants.Config.DEFAULT_PORTS, and decides
                      whether or not the ports inputted are saved into the local file or not.

        The proper data types for each ID are as follows:
        - DO_PRINT: data should be a boolean
        - DEFAULT_PORTS: data should be a list, of valid integer ports

        Example: 
            >>> inst = Lynxy()
            >>> inst.set_config(lynxy.Constants.Config.DEFAULT_PORTS, [111, 222, 333])
        '''
        # make sure the data types are not invalid
        # to prevent errors later on
        # if all pass, then change data
        if ID == Constants.Config.DO_PRINT and type(data) != bool: raise Exceptions.InvalidToggleValueError()
        elif ID == Constants.Config.DEFAULT_PORTS:
            if type(data) != list: raise Exceptions.InvalidToggleValueError()
            for indiv_port in data: 
                if type(indiv_port) != int: raise Exceptions.InvalidToggleValueError()
        # save the data into the config dictionary
        self.config[ID] = data
        # if the file save is enabled, save ports to file
        if save_ports: 
            with open(os.path.join(self.wDir, 'config.json', 'r')) as f:
                config_data = json.load(f)
            config_data[Constants.Config.DEFAULT_PORTS] = data
            with open(os.path.join(self.wDir, 'config.json', 'w')) as f:
                json.dump(config_data, f)
        return None
    

    # a function used to distinguish whether or not to print,
    # different from the default printing function but not overwriting it
    def pprint(self, data: str): 
        if self.config[Constants.Config.DO_PRINT]: print(data)
        return None
    

    # this is the function that connects to the other end
    # def connect(self, connection_type: Constants.Connection):
    #     # first we must remake the client
    #     # this is essential every time we connect
    #     self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     # for each port, we need to try to connect to it
    #     valid_ports = self.config[Constants.Config.DEFAULT_PORTS]
    #     for port in valid_ports: