'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION
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

    class InvalidToggleValueError(Exception):
        def __init__(self, message='The ID and value toggle pair is invalid.'):
            self.message = message
            super().__init__(message)

    
    class EmptyDataError(Exception):
        def __init__(self, message='The data you attempted to send is empty.'):
            self.message = message
            super().__init__(message)


    class TerminationSuccessError(Exception):
        def __init__(self, message='Connection was terminated successfully!'):
            self.message = message
            super().__init__(message)

         
    class InvalidPortError(Exception):
        def __init__(self, message=None):
            self.message = message
            super().__init__(message)


    class ConnectionFailedError(Exception):
        def __init__(self, message=None):
            self.message = message
            super().__init__(message)

    
    class NoEventError(Exception):
        def __init__(self, message=None):
            self.message = message
            super().__init__(message)