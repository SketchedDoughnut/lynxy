from src import lynxy

hport = 56776

client = lynxy.Lynxy(['', hport], bind=True)

print('this clients credentials are:')
print(client.get_host())

ip = '192.168.68.118'
port = 56775

client.start_logging()

input('confirm start connect')

client.connect([ip, port])

@client.event(lynxy.Constants.Event.ON_CONNECT)
def my_function(connect_state: bool):
     print(connect_state)

@client.event(lynxy.Constants.Event.ON_MESSAGE)
def my_function(message: lynxy.Pool.Message):
     print(message.content)

@client.event(lynxy.Constants.Event.ON_CLOSE)
def my_function(error: lynxy.Exceptions.BaseLynxyException | None):
     print(error)

while True: 
     input('confirm close')
     break
client.close()