'''
this file intends to start the inbound client
'''

import socket

def start_inbound(ip: str) -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # set up client obj
    client.connect(ip) # connect to inputted IP of other person 
