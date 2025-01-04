from src import lynxy

# set up lynxy client
client = lynxy.Lynxy(bind=True)
print(client.get_host())

source = r'D:\VScode\github practice\filter\original\die.mp4'

target = ['192.168.68.113', 56774]
client.connect(target)

f = open(source, 'rb')
contents = f.read()
f.close()

client.send(contents)

while True:
    input('-> ')
    break

client.close()