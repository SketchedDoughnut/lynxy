from src import lynxy
from rich import print

inst = lynxy.Lynxy(host_port=11112, bind=True)
host = inst.get_host()
target = ('192.168.68.130', 11111)
inst.connect(target)

print('connected')
print(f'host: {host}')
print(f'target: {target}')

@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def recv(msg: lynxy.Pool.Message): 
    # print(msg.content)
    print(f'{msg.created_at} -> {msg.recieved_at}')

@inst.event(lynxy.Constants.Event.ON_CLOSE)
def close(msg):
    print('connection closed:', msg)
    inst.close()

while True:
    msg = input('-> ')
    if msg == 'exit': 
        inst.close()
        break
    inst._comm._send(msg)