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
        self.endMarker = ':~e~:'


    # this function prepares messages to be sent
    # takes in an input of the encrypted data and returns
    # it in a string with the start marker
    def addPadding(self, message: any) -> str: return f'{message}{self.endMarker}'


    # this function splits the messages by the start marker
    # and can optionally discard invalid endings that aren't complete
    def removePadding(self, message: str, remove_invalid: bool = True) -> list:
        # split into list, remove empty entries
        # only if remove_invalid is True
        splitMessage = message.split(self.endMarker)
        if len(splitMessage[-1]) == 0: splitMessage.pop(-1)
        if remove_invalid and not message.endswith(self.endMarker): splitMessage.pop(-1)
        # go through and convert each message in the list
        # into bytes instead of strings
        finalList = []
        for elem in splitMessage: finalList.append(literal_eval(elem))
        return finalList