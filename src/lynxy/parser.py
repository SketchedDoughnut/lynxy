'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION
'''

# included modules
# from ast import literal_eval

# external modules
pass

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
    def removePadding(self, message: bytes, remove_empty: bool = True) -> list:
        '''
        basically how this works:
        When we split a message into a list, it has a whitespace where every end marker is.
        This is an empty entry in the list. We can check if the last entry in the list is empty.
        If it is, this means that there was an end marker. Otherwise, this means that that is an incomplete piece,
        and we can save that to self.carry for the next cycle.
        '''
        # split message by end marker
        splitMessage = message.split(self.byteEndMarker)
        # saving incomplete packets
        # if last marker is not zero, save to carry and remove
        if not message.endswith(self.byteEndMarker): self.carry = splitMessage.pop(-1)
        # if toggled, remove all empty entries
        if remove_empty:
            index = 0
            for elem in splitMessage:
                if len(elem) == 0: splitMessage.pop(index)
                index += 1
        return splitMessage