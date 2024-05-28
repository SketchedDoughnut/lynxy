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















from src import lynxy as l
from src import lynxy_server as ls

# ls.disable_print()
ip, port, token = ls.start_server()
l.enable_print()
l.start_client(ip)
l.send_msg('username SketchedDoughnut')
l.request_username_data('SketchedDoughnut')
l.submit_username_data('SketchedDoughnut')
l.send_msg(f'auth {token}')
l.send_msg('end_session')
l.shutdown_client()