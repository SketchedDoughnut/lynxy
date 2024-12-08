from src import lynxy

inst = lynxy.Lynxy(host_port=11111, bind=True)
connect_ip = input('-> ')
connect_port = int(input('-> '))
inst.connect(connect_ip, connect_port)