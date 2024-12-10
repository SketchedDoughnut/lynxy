from src import lynxy

inst = lynxy.Lynxy(bind=True)
print(inst.get_host())
inst.connect(inst.get_host()[0], inst.get_host()[1])
print('connected!')
print('external pub:', inst.comm.sec.ext_pub_key)