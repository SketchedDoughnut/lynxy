from src import lynxy as l

def run_client(ip):
    l.enable_print()
    # ip = input('-> ')
    print('state of connect:', l.start_client(ip))
    while True:
        msg = input('-> ')
        # msg = 't'
        if msg == 'break':
            break
        # elif msg == 'token':
        #     l.send_msg(f'auth {token}')
            continue
        l.send_msg(msg)
    l.shutdown_client()


# running
run_client(input('-> '))