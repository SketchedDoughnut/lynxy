'''
PUT INTRODUCTORY HEADER HERE, INCLUDE ANY OTHER INFORMATION
'''

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
        splitMessage = message.split(self.endMarker)
        if len(splitMessage[-1]) == 0: splitMessage.pop(-1)
        if remove_invalid and not message.endswith(self.endMarker): splitMessage.pop(-1)
        return splitMessage