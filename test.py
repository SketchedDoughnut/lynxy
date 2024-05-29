from src import lynxy_server as ls
from src import lynxy as l

ip = '127.0.0.1'
ls.override_ip(ip)
ls.start_server()
l.enable_print()
l.start_client(ip)
l.submit_username_data('SketchedDoughnut')
l.submit_username_data('SketchedDoughnut')