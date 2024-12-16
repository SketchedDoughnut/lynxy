from src import lynxy
from rich import print
inst = lynxy.Lynxy()

@inst._comm.event(lynxy.Constants.Event.ON_MESSAGE)
def test(input): print(input)
inst._comm._trigger(lynxy.Constants.Event.ON_MESSAGE, 'test')