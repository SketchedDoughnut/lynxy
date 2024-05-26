from src import lynxy as l
from src import lynxy_server as ls

# ls.disable_print()
ip, port, auth_token = ls.start_server()

l.start_client(input())
while True:
    l.general_send(input())