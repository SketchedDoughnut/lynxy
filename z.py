from src import lynxy as l
from src import lynxy_server as ls

ls.disable_print()
ip, port = ls.start_server()
# ls.shutdown_server()

l.start_client('IP')
l.shutdown_client()
# this is just bullying the server but point is it works
# ln = 5000
# ln = 1
# for i in range(ln):
#     l.submit_username_data(f'SketchedDoughnut-{i}')
#     l.request_username_data(f'SketchedDoughnut-{i}')