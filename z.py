from src import lynxy as l
from src import lynxy_server as ls

# ls.disable_print()
ip, port, auth_token = ls.start_server()
# print(ip, port, auth_token)

l.start_client(input())
while True:
    msg = input()
    l.general_send(msg)