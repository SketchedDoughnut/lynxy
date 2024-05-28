# import lynxy

# lynxy.enable_print()
# ip = input('-> ')
# lynxy.start_client(ip)
# while True:
#     msg = input('-> ')
#     # msg = 't'
#     if msg == 'break':
#         break
#     lynxy.send_msg(msg, recieve=True)
# lynxy.shutdown_client()

# import lynxy_server as ls
from src import lynxy_server as ls

ip, port, token = ls.start_server()

from src import lynxy as l
l.enable_print()
l.start_client(ip)
l.send_msg(" ", recieve=True)
l.send_msg('username', recieve=True)
l.send_msg('username SketchedDoughnut', recieve=True)
l.send_msg('clear_client', recieve=True)