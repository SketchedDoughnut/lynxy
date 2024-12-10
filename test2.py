from src import lynxy

def c2():
    inst = lynxy.Lynxy(host_port=11112, bind=True)
    print('initialized...')
    print(inst.comm.get_host())
    connect_ip = '192.168.68.123'
    connect_port = 11111
    print('connecting...')
    inst.connect(connect_ip, connect_port)
    print('connected')
    inst.close()
    print('closed')

c2()