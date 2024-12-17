from src import lynxy
from rich import print
inst = lynxy.Lynxy()

@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def test(input): print(input)
inst._comm._trigger(lynxy.Constants.Event.ON_MESSAGE, 'test')

print(inst._comm.eventRegistry)


data = b'dasfasdfas'
print(data.split(b':~e~:'))