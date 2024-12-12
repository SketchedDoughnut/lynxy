from src import lynxy
from rich import print
import threading

def c2():
    inst = lynxy.Lynxy(host_port=11112, bind=True)
    print('initialized...')
    print(inst.get_host())
    connect_ip = '192.168.68.114' #
    connect_port = 11111 #
    print('connecting...')
    inst.connect(connect_ip, connect_port)
    print('connected')
    print(inst.get_actual_target())
    threading.Thread(target=lambda:inst.comm._recv()).start()
    while True:
        inst.send(input('-> '))
    inst.close()
    print('closed')
c2()