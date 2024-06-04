from src import lynxy_server as ls

ls.set_encrypt_client_data(False)
ip, port, token = ls.start_server()

from src import lynxy as l

import time


l.enable_print()
l.start_client(ip)
# l.submit_username_data('SketchedDoughnut')
# l.submit_username_data('SketchedDoughnut')
# d = l.request_username_data('SketchedDoughnut')
l.send_msg('listener', recieve=False)
l.start_client_listener()
for i in range(10):
    msg = 'LARGE data like this is a lot of data i am sending over the internet to the server, oh boy~!'
    l.send_msg(msg, recieve=False)
    time.sleep(0.025)
# print(ls.get_data())
print(l.get_data())