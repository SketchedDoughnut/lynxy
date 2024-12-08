from src import lynxy

inst = lynxy.Lynxy(host_port=11111, bind=True)
print('initialized...')
print(inst.comm.get_host())
connect_ip = input('-> ')
connect_port = int(input('-> '))
print('connecting...')
inst.connect(connect_ip, connect_port)
inst.close()