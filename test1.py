from src import lynxy
import threading
from rich import print
import datetime

inst = lynxy.Lynxy(host_port=11111, bind=True)
host = inst.get_host()
target = ('192.168.68.114', 11112)
print(f'host: {host}')
print(f'target: {target}')
print('connecting...')
inst.connect(target[0], target[1])
print('connected')
threading.Thread(target=lambda:inst._comm._recv2()).start()
print('recieving')
@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def recv(msg): 
    print(msg)
while True:
    # inst._comm._send2(input('-> '))
    current = datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y, %H:%M:%S")
    inst._comm._send2(current)
    print('sending:', current)
    input('-> ')