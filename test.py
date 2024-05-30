from src import lynxy_server as ls

ip, port, token = ls.start_server()

from src import lynxy as l

l.enable_print()
l.start_client(ip)
l.send_msg('listener')
for i in range(5):
    l.send_msg(f'test-{i}')
print(ls.get_data())