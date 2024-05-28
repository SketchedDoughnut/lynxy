# import lynxy

# lynxy.enable_print()
# ip = input('-> ')
# lynxy.start_client(ip)
# while True:
#     msg = input('-> ')
#     # msg = 't'
#     if msg == 'break':
#         break
#     lynxy.send_msg(msg, recieve=True)
# lynxy.shutdown_client()















from src import lynxy as l

ip = input('-> ')
l.enable_print()
l.start_client(ip)
l.submit_username_data('SketchedDoughnut')
input('-> ')
data = l.request_username_data('laptop')
i = data[0]
p = data[1]
print(i)
print(p)
l.shutdown_client()
input('-> ')
print(l.target_client(i, p))