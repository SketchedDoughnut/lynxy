# from src import lynxy as l
# from src import lynxy_server as ls




# # server
# ls.disable_print()
# ip, port, auth_token = ls.start_server()

# # client
# l.disable_print()
# l.start_client(ip)
# l.general_send(f'{auth_token}')
# l.general_send('freeze_server')
# l.general_send(f'auth {auth_token}')
# l.submit_username_data('SketchedDoughnut')
# l.request_username_data('SketchedDoughnut~!')
# print(l.request_username_data('SketchedDoughnut')) # will work


# print(ls.freeze_server())
# l.general_send('username test')


# import lynxy_server as ls

# # ls.disable_print()
# ip, port, token = ls.start_server()

# import lynxy as l

# l.disable_print()
# l.start_client(ip)
# l.submit_username_data('SketchedDoughnut')
# l.request_username_data('SketchedDoughnut')
# l.general_send(f'auth {token}')
# ls.freeze_server()
# l.general_send('ping')
# l.start_client(ip)

import lynxy

lynxy.enable_print()
ip = input('-> ')
lynxy.start_client(ip)
lynxy.submit_username_data('SketchedDoughnut')
# lynxy.request_username_data('SketchedDoughnut')
lynxy.submit_username_data('SketchedDoughnut2')
lynxy.request_username_data('SketchedDoughnut3') # incorrect username
lynxy.request_username_data('SketchedDoughnut')
lynxy.send_msg('end_session')
lynxy.shutdown_client()