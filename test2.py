from src import lynxy
import threading
from rich import print
import datetime

inst = lynxy.Lynxy(host_port=11112, bind=True)
host = inst.get_host()
target = ('192.168.68.130', 11111)
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
while True:
    # inst._comm._send(input('-> '))
    current = datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y, %H:%M:%S")
    inst._comm._send(current)
    print('sending:', current)
    # input('-> ')