# import lynxy as l
# import lynxy_server as ls

from src import lynxy as l
from src import lynxy_server as ls

def run_server():
    # ls.set_encrypt_client_data(False)
    ip, port, token = ls.start_server()
    return (ip, port, token)

def run_client(ip):
    respond_mode = True
    l.enable_print()
    # ip = input('-> ')
    print('state of connect:', l.start_client(ip))
    while True:
        msg = input('-> ')
        # msg = 't'
        if msg == 'break':
            break
        elif msg == 'token':
            l.send_msg(f'auth {token}')
            continue
        elif msg == 'listener':
            respond_mode = False
        l.send_msg(msg, respond_mode)
    l.shutdown_client()


# running
ip, port, token = run_server()
run_client(ip)