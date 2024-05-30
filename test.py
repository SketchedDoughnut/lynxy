from src import lynxy_server as ls
from src import lynxy as l

def func(msg: str, addr: str) -> str:
    print('msg:', msg)
    print('addr:', addr)

ls.load_function(func)
ip, port, token = ls.start_server()

l.start_client(ip)
l.send_msg('tester')