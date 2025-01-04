from src import lynxy

# set up lynxy client
client = lynxy.Lynxy(bind=True)
print(client.get_host())

out = r'D:\VScode\packages\lynxy\recieved.mp4'

target = ['192.168.68.129', 56774]
client.connect(target)

@client.event(lynxy.Constants.Event.ON_MESSAGE)
def on_message(data: lynxy.Pool.Message):
    f = open(out, 'wb')
    f.write(data.content)
    f.close()