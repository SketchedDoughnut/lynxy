from src import lynxy

hport = 56775

client = lynxy.Lynxy(['', hport], bind=True)

print('this clients credentials are:')
print(client.get_host())

ip = '192.168.86.53'
port = 56776

# client.start_logging()

input('confirm start connect')

client.connect([ip, port])

@client.event(lynxy.Event.ON_CONNECT)
def my_function(connect_state: bool):
     print('connected!')
     client.send('hi from test 1!')
     print('state of connection:', connect_state)

@client.event(lynxy.Event.ON_MESSAGE)
def my_function(message: lynxy.Message):
     print('new message:', message.content)

@client.event(lynxy.Event.ON_CLOSE)
def my_function(error: Exception | None):
     print('closed:', error)

while True: 
     input('confirm close')
     break
client.close()