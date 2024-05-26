from src import lynxy as l
from src import lynxy_server as ls




# server
# ls.disable_print()
ip, port, auth_token = ls.start_server()

# client
l.disable_print()
l.start_client(input('-> '))
l.general_send(f'{auth_token}')
l.general_send('freeze_server')
l.general_send(f'auth {auth_token}')
l.submit_username_data('SketchedDoughnut')
l.request_username_data('SketchedDoughnut~!')
print(l.request_username_data('SketchedDoughnut')) # will work


print(ls.freeze_server())
l.general_send('username test')