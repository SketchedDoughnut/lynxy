'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION
'''

# included modules
# from ast import literal_eval

# external modules
from rich import print

####################################################

# this is the main class for the parser 
class Parser:
    def __init__(self): 
        # end marker for message
        self.byteEndMarker = b':~e~:'
        # carry over from previous incomplete packets
        self.carry = b''


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
        split = message.split(self.byteEndMarker)
        print('split:', split)
        # if the end characters is the end marker, then that means
        # we only have complete messages so we can reset carry
        if message.endswith(self.byteEndMarker):
            print('ends with marker, clearing carry')
            self.carry = b''
        # otherwise, we analyze further
        else:
            # if the length of the list is 0, then we have nothing
            # if the length of the list is 1, the we only have
            # a singular incomplete packet
            if len(split) <= 1:
                # save the message to carry and return
                # empty list
                print('length is 1, saving to carry')
                self.carry = message
                return []
            # else, if the last entry of the list is empty
            # if it is empty, this means there was a split there
            # if it isn't empty, that means there is an incomplete packet
            elif split[-1]: # meaning there is content
                # take the last thing of content and save to carry
                print('content found in last entry, saving to carry')
                self.carry = split.pop(-1)
        # if requested, go ahead and remove all white spaces
        if remove_empty:
            index = 0
            for elem in split:
                if not elem: 
                    print('removing:', index)
                    split.pop(index)
                index += 1
        print('returning:', split)
        return split