from src import lynxy
from rich import print

inst = lynxy.Lynxy(('', 11111), True)
print('initialized')
host = inst.get_host()
target = ('192.168.68.124', 11112)

print(f'host: {host}')
print(f'target: {target}')

inst.connect(target)
print('connected')


@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def recv(msg: lynxy.Pool.Message): 
    print(f'{msg.created_at} -> {msg.recieved_at}')
    # print(f'{msg.created_at} -> {msg.recieved_at}: {msg.content}')

@inst.event(lynxy.Constants.Event.ON_CLOSE)
def close(msg):
    print('connection closed:', msg)
    inst.close()

# while True:
#     msg = input('-> ')
#     if msg == 'exit': 
#         inst.close()
#         break
#     inst._comm._send(msg)

# https://courses.cs.washington.edu/courses/cse163/20wi/files/lectures/L04/bee-movie.txt
with open(r'D:\VScode\packages\lynxy\bee.txt', 'r') as f:
    contents = f.read()
print(len(contents))
inst.send(contents)
while True:
    input('-> ')
    break
inst.close()