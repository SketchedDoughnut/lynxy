# from src import lynxy
import lynxy
from rich import print

inst = lynxy.Lynxy(bind=True)
print('initialized')
host = inst.get_host()
target = ('192.168.68.113', 56774)

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

## uncomment for sending bee movie, comming out above while loop

# # https://courses.cs.washington.edu/courses/cse163/20wi/files/lectures/L04/bee-movie.txt
# with open(r'D:\VScode\packages\lynxy\bee.txt', 'r') as f:
#     contents = f.read()
# print(len(contents))
# inst.send(contents)

# while True:
#     input('-> ')
#     break
# inst.close()