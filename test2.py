from src import lynxy
from rich import print

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
    print('int pub:', inst.comm.sec.int_pub_key)
    print('int priv:', inst.comm.sec.int_priv_key)
    print('ext pub:', inst.comm.sec.ext_pub_key)
    inst.send('test!')
    inst.close()
    print('closed')
c2()