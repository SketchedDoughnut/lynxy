from src import lynxy

hport = 56776

client = lynxy.Lynxy(['', hport], bind=True)

print('this clients credentials are:')
print(client.get_host())

ip = '192.168.86.53'
port = 56775

# client.start_logging()

@client.event(lynxy.Event.ON_CONNECT)
def my_function(connect_state: bool):
     print('connected!')
     client.send('hi from test 2!')
     print('state of connection:', connect_state)

@client.event(lynxy.Event.ON_MESSAGE)
def my_function(message: lynxy.Message):
     print('new message:', message.content)

@client.event(lynxy.Event.ON_CLOSE)
def my_function(error: Exception | None):
     print('closed:', error)

# connect
input('confirm start connect')
client.connect([ip, port])
while True: 
     input('confirm close')
     break
client.close()