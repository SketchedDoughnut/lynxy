from src import lynxy
import threading
from rich import print

inst = lynxy.Lynxy(bind=True)
host = inst.get_host()
target = ('', 0)
print(f'host: {host}')
print(f'target: {target}')
print('connecting...')
inst.connect(target[0], target[1])
print('connected')
threading.Thread(target=inst._comm._recv2()).start()
@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def recv(msg): print(msg)
while True:
    inst.send(input('-> '))