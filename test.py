from src import lynxy as l
from src import lynxy_server as ls

# start server
ls.disable_print()
ip, port, token = ls.start_server()

 # start client
l.enable_print()
l.start_client(ip)

# print('ACQUIRED:', l.send_msg('listener'))
# l.submit_username_data('SketchedDoughnut')
# l.request_username_data('SketchedDoughnut')

# put client into listening mode
l.send_msg('listener')

# send over data packets
for i in range(5):
    # print('ACQUIRED:', l.send_msg(f'test-{i}'))
    msg = f'{i}' + 'x' * 1000
    res = l.send_msg(msg).encode()
    import sys
    print('incoming size:', sys.getsizeof(res))
print(ls.get_data())