'''
This is the pool file, which contains a variety of different types of objects used for variables or recieved data.
For example, on the client ON_MESSAGE, the data you recieve is a Pool.Message object.
'''

# libraries
from datetime import datetime

# this is a class of different helpful features
class Util:
    def _format_time() -> str: return datetime.strftime(datetime.now(), "%d/%m/%Y, %H:%M:%S")
    

# this is a class for message objects
class Message:
    '''
    This class represents a Lynxy.Message object, which is what is
    used for sending data from one machine to the other. The Message object
    has 4 attributes:

    Attributes
    ----------
    content: any
        The actual data that was meant to be sent

    created_at: str
        The timestamp for when the message object was created on the sending side

    recieved_at: str
        The timestamp for when the message object was recieved on the recieving side

    public_key: rsa.PublicKey
        The public key used to encrypt this message object when sent
    '''
    def __init__(self, data):
        self.content = data
        self.created_at = Util._format_time()
        self.recieved_at = None