from src import lynxy

def c1():
    inst = lynxy.Lynxy(host_port=11111, bind=True)
    print('initialized...')
    print(inst.comm.get_host())
    connect_ip = '192.168.68.124'
    connect_port = 11112
    print('connecting...')
    inst.connect(connect_ip, connect_port)
    inst.close()

def c2():
    inst = lynxy.Lynxy(host_port=11112, bind=True)
    print('initialized...')
    print(inst.comm.get_host())
    connect_ip = '192.168.68.123'
    connect_port = 11111
    print('connecting...')
    inst.connect(connect_ip, connect_port)
    inst.close()

c1()
# c2()