'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION
'''

# included modules
from datetime import datetime

# the main class for containing all of the types of stuff
class Pool:

    # this is a class of tools
    class Tools:
        def _format_time() -> str: return datetime.strftime(datetime.now(), "%d/%m/%Y, %H:%M:%S")
        

    # this is a class for creating message objects
    class Message:
        def __init__(self, data, pub_key):
            self.content = data
            self.created_at = Type.Tools._format_time()
            self.recieved_at = None # set on recieving end
            self.public_key = pub_key