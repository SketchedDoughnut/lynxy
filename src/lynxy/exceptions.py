'''
This is the exceptions file, which contains all of the Exceptions that are raised throughout the code.
These are helpful to know in case you want to catch any errors when doing a variety of different functions.
'''

# this is the class for all errors
# which contains all other classes of errors
class Exceptions:
    class ClientNotConnectedError(Exception):
        def __init__(self, message='The client is not connected.'):
            self.message = message
            super().__init__(message)

    class NoExteralPublicKeyError(Exception):
        def __init__(self, message='External public key has not been loaded.'):
            self.message = message
            super().__init__(message)

    
    class EmptyDataError(Exception):
        def __init__(self, message='The data you attempted to send is empty.'):
            self.message = message
            super().__init__(message)


    class ConnectionFailedError(Exception):
        def __init__(self, message=None):
            self.message = message
            super().__init__(message)