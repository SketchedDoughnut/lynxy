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
from .constants import Constants
from .exceptions import Exceptions
from .sec import Sec

####################################################

# the main class for the connection
class Lynxy:
    def __init__(self):
        '''
        This is a class that represents a handler for connecting
        to any other end you intend to, whether that be another client, server, or lynxy server.
        This class has all the configuration and management for your client instance.
        '''
        # this is the current working directory
        self.wDir = os.path.dirname(os.path.abspath(__file__))
        # this is an instance of the security manager 
        self.sec = Sec()
        # this dictionary contains all of the configurable things
        # accessible by the user.
        # this is loaded farther down
        self.config = {}
        # this is the IP used for the connection
        self.host = ''
        # this is the port used for the connection
        self.port = None
        # this is the client used for sending and recieving
        self.client = None
        # this represents if the client is connected
        self.is_connected = False
        # here we load the valid ports
        self.load_config()


    # a function to load the config.json file
    def load_config(self):
        with open(os.path.join(self.wDir, 'config.json'), 'r') as f: self.config = json.load(f)
        

    # a function for setting the externally configurable data
    def set_config(self, ID: Constants.Config, data: bool | list[int], save_to_file: bool = False) -> None:
        '''
        This function allows you to configure certain internal values.
        - ID: is used as a key in a dictionary to find out what data to change.
              The ID is from lynxy.Constants.Config, and should match with the data you
              are inputting. For example, if ID is lynxy.Constants.Config.VALID_PORTS, 
              then data should be a list of integer ports.
        - data: is used for changing the actual data in the config dictionary. As 
                previously mentioned, your data type must match up with the inputted
                ID.
        - save_to_file: is used to decide whether or not to save the data to file that is
                        loaded for each use.

        The proper data types for each ID are as follows:
        - DO_PRINT: data should be a boolean
        - VALID_PORTS: data should be a list, of valid integer ports

        Example: 
            >>> inst = Lynxy()
            >>> inst.set_config(lynxy.Constants.Config.VALID_PORTS, [111, 222, 333])
        '''
        # check if the DO_PRINT data is invalid
        if ID == Constants.Config.DO_PRINT and type(data) != bool: raise Exceptions.InvalidToggleValueError()
        # check if the VALID_PORTS data is invalid
        elif ID == Constants.Config.VALID_PORTS:
            # if not a list, invalid
            if type(data) != list: raise Exceptions.InvalidToggleValueError()
            # verify each port within the list
            for indiv_port in data: 
                # if not an int, invalid
                if type(indiv_port) != int: raise Exceptions.InvalidPortError('The port is not an integer.')
                # if port is 0, invalid (I believe this is saved for TCP?)
                if indiv_port == 0: raise Exceptions.InvalidPortError('Ports cannot be 0.')
        # save the data into the config dictionary
        self.config[ID] = data
        # if the save_ports is enabled, save ports to file
        if save_to_file: 
            with open(os.path.join(self.wDir, 'config.json'), 'w') as f: 
                json.dump(self.config, f)
        return None
    

    # a function used to distinguish whether or not to print,
    # different from the default printing function but not overwriting it
    def pprint(self, data: str): 
        if self.config[Constants.Config.DO_PRINT]: print(data)
        return None
    

    # this is the function that connects to the other end
    def connect(self) -> tuple[bool, str, int, socket.socket]:
        '''
        This function connects to the other end. This is helpful if you don't want
        the client to do anything after establishing a connection. However, for connecting
        to another lynxy client or a lynxy server, the login function should be used instead.
        All this does is run connect, then sec.RSA_handhsake.
        '''
        # first we must remake the client
        # this is essential EVERY time we connect
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get the valid ports and the IP we are going to use
        valid_ports = self.config[Constants.Config.VALID_PORTS]
        if self.config[Constants.Config.IP_OVERRIDE] != None: active_ip = self.config[Constants.Config.IP_OVERRIDE]
        else: active_ip = self.host
        # cycle over each port, trying them
        for port in valid_ports:
            self.pprint(f'Trying (port:ip) - {active_ip}:{port}...')
            try:
                # attempt to connect, if success this will continue
                # otherwise try to catch some errors that are fine, if 
                # they are other errors then let them happen
                self.client.connect((active_ip, port))
                self.is_connected = True
                self.host = active_ip
                self.port = port
                return (self.is_connected, self.host, self.port, self.client)
            except ConnectionRefusedError: 
                self.pprint('Target machine refused, cycling... (ConnectionRefusedError)')
            except TimeoutError: 
                self.pprint('Target machine timed out, cycling... (TimeoutError)')
        # failed :c
        return (self.is_connected, None, None, None)


    # this is a function that connects, but then also does a handshake
    # exchanging RSA keys
    # TODO
    def login(self):
        if not self.is_connected: self.connect()