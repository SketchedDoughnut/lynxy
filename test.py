from src import lynxy_server as ls
from src import lynxy as l

ip = '127.0.0.1'
ls.override_ip(ip)
ls.start_server()
l.enable_print()
l.start_client(ip)
l.submit_username_data('SketchedDoughnut')
l.submit_username_data('SketchedDoughnut')
l.shutdown_client()
exit()
import time
time.sleep(2.5)
print('Restarting...')
time.sleep(2.5)
l.start_client(ip)
l.request_username_data('SketchedDoughnut')