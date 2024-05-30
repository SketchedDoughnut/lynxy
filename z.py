import lynxy as l
import lynxy_server as ls

def run_server():
    ip, port, token = ls.start_server()
    return (ip, port, token)


# running
ip, port, token = run_server()

l.enable_print()
# ip = input('-> ')
ip = ip
print('state of connect:', l.start_client(ip))
while True:
    msg = input('-> ')
    # msg = 't'
    if msg == 'break':
        break
    l.send_msg(msg, recieve=True)
l.shutdown_client()