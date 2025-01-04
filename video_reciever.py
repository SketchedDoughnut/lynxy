from src import lynxy
import time

# set up lynxy client
client = lynxy.Lynxy(bind=True)
client.set_connection(lynxy.Constants.ConnectionType.ERROR)
print(client.get_host())

out = r'recieved.mp4'

target = ['192.168.68.129', 56774]
client.connect(target)

@client.event(lynxy.Constants.Event.ON_MESSAGE)
def on_message(data: lynxy.Pool.Message):
    f = open(out, 'wb')
    f.write(data.content)
    f.close()

time.sleep(1)

client.close()