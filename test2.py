# from src import lynxy
import lynxy
from rich import print

inst = lynxy.Lynxy(bind=True)
print('initialized')
host = inst.get_host()
target = ('192.168.68.129', 56774)

print(f'host: {host}')
print(f'target: {target}')

inst.connect(target)
print('connected')

@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def recv(msg: lynxy.Pool.Message): 
    print(msg.content)

@inst.event(lynxy.Constants.Event.ON_CLOSE)
def close(msg):
    print('connection closed:', msg)

while True:
    msg = input('-> ')
    if msg == 'exit': 
        inst.close()
        break
    inst.send(msg)