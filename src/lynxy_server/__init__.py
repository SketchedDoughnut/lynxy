'''
This is the lynxy server module. To find documentation, go to the github~!
- Github: https://github.com/SketchedDoughnut/LYNX
'''

# extending main lynx file
from .lynx_server import *

def help(open_tab: bool = False) -> str:
    '''
    A function that returns a link to the Github page
    '''
    if open_tab == True:
        import webbrowser
        webbrowser.open_new_tab('https://github.com/SketchedDoughnut/LYNX')
    else:
        return 'https://github.com/SketchedDoughnut/LYNX'
    
def license(open_tab: bool = False) -> str:
    '''
    A function that returns a link to the license this project is under
    '''
    if open_tab == True:
        import webbrowser
        webbrowser.open_new_tab('https://github.com/SketchedDoughnut/LYNX/blob/master/LICENSE')
    else:
        return 'https://github.com/SketchedDoughnut/LYNX/blob/master/LICENSE'
    
def credits() -> str:
    '''
    A function that returns a string containing the credits for this project
    '''
    return 'This project is developed and maintained by SketchedDoughnut'