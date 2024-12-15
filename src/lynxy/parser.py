'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION
'''

# included modules
from ast import literal_eval

####################################################

# this is the main class for the parser 
class Parser:
    def __init__(self): 
        # start marker for message
        self.stringEndMarker = ':~e~:'
        self.byteEndMarker = b':~e~:'
        self.carry = b'' # carry over from previous incomplete packets


    # this function prepares messages to be sent
    # takes in an input of the encrypted data and returns
    # it in a string with the start marker
    def addPadding(self, message: bytes) -> bytes: return message + self.byteEndMarker


    # this function splits the messages by the start marker
    # and can optionally discard invalid endings that aren't complete
    def removePadding(self, message: bytes) -> list:
        # split message by end marker
        splitMessage = message.split(self.byteEndMarker)
        # remove empty values at the end, its usually wherever
        # the split happened
        if len(splitMessage[-1]) == 0: splitMessage.pop(-1)

        # TODO
        # handle incomplete packets at end
        # for now just considered lost

        return splitMessage