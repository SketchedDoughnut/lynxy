from src import lynxy as l
from src import lynxy_server as ls

l.disable_print()
ls.start_server()
l.start_client('IP GOES HERE')

# this is just bullying the server but point is it works
for i in range(5000):
    l.submit_username_data(f'SketchedDoughnut-{i}')
    l.request_username_data(f'SketchedDoughnut-{i}')