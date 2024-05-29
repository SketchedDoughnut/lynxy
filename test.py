from src import lynxy_server as ls
from src import lynxy as l

ip = '127.0.0.1'
username = 'SketchedDoughnut'
ls.override_ip(ip)
ls.start_server()
l.enable_print()
l.start_client(ip)
l.submit_username_data(username)
l.submit_username_data(username)
l.shutdown_client()
# exit()
import time
print('Restarting...')
# t = 60 * 4
t = 5
for i in range(1, t, 1):
    print(f'{i}/{t}')
    time.sleep(1)
result = l.start_client(ip)
if result:
    l.request_username_data(username)

print(ls.get_data())