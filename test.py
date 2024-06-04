from src import lynxy_server as ls

ls.set_encrypt_client_data(False)
ip, port, token = ls.start_server()

from src import lynxy as l

l.enable_print()
l.start_client(ip)
l.submit_username_data('SketchedDoughnut')
l.submit_username_data('SketchedDoughnut')
d = l.request_username_data('SketchedDoughnut')
print(ls.get_data())