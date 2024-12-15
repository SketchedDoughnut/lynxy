from src import lynxy
from rich import print
import threading
import datetime
import time

def c1():
    inst = lynxy.Lynxy(host_port=11111, bind=True)
    print('initialized...')
    print(inst.get_host())
    connect_ip = '192.168.68.124' #
    connect_port = 11112 #
    print('connecting...')
    inst.connect(connect_ip, connect_port)
    print('connected')
    print(inst.get_actual_target())
    # get stuck in recv loop
    threading.Thread(target=lambda:inst.comm._recv()).start()
    while True:
        # inst.send(input('-> '), True)
        inst.send(datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y, %H:%M:%S"))
        time.sleep(0.5)
    inst.close()
    print('closed')
c1()

# 10 screen off, 30 pc sleep