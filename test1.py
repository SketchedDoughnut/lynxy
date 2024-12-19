from src import lynxy
import threading
from rich import print

inst = lynxy.Lynxy(host_port=11111, bind=True)
host = inst.get_host()
target = ('192.168.68.114', 11112)
print(f'host: {host}')
print(f'target: {target}')
print('connecting...')
inst.connect(target)
print('connected')
# threading.Thread(target=lambda:inst._comm._recv2()).start()
# print('recieving')
@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def recv(msg): 
    print(msg)
    pass
while True:
    inst._comm._send(input('-> '))