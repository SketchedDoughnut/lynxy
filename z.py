import lynxy

lynxy.enable_print()
ip = input('-> ')
lynxy.start_client(ip)
while True:
    msg = input('-> ')
    # msg = 't'
    if msg == 'break':
        break
    lynxy.send_msg(msg, recieve=True)
lynxy.shutdown_client()


# from src import lynxy as l

# ip = input('-> ')
# l.start_client(ip)
# l.submit_username_data('1')
# input('-> ')
# data = l.request_username_data('2')
# ip = data[0]
# port = data[1]
# l.shutdown_client()
# print(l.target_client(ip, port, 'idk'))