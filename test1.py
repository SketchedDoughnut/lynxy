from src import lynxy
import threading
from rich import print

inst = lynxy.Lynxy(host_port=11111, bind=True)
inst.set_connection(lynxy.Constants.ConnectionType.RETRY)
host = inst.get_host()
target = ('192.168.68.114', 11112)
print(f'host: {host}')
print(f'target: {target}')
print('connecting...')
inst.connect(target)
print('connected')
@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def recv(msg: lynxy.Pool.Message): 
    print(msg.content)
    print(msg.created_at)
    print(msg.recieved_at)
@inst.event(lynxy.Constants.Event.ON_CLOSE)
def close(msg):
    print(msg)
while True:
    inst._comm._send(input('-> '))