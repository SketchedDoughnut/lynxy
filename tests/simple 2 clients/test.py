# import lynxy
from src import lynxy

# create our client
host = ('', 56775)
client = lynxy.Client(host=host)

# add our on_connect event
@client.event(lynxy.Event.ON_CONNECT)
def my_function(connect_state: bool):
     print(connect_state)

# add our on_message event
@client.event(lynxy.Event.ON_MESSAGE)
def my_function(message: lynxy.Message):
     print(message.content)

# add our on_close event
@client.event(lynxy.Event.ON_DISCONNECT)
def my_function(error: lynxy.Exceptions.BaseLynxyException| None):
     print(error)

# connect to the other computer using its IP and port
# both clients need to be ready to connect in order for a connection to work
target = ('192.168.86.53', 56776)
input('awaiting connect confirmation:')
client.connect(target)

# send messages, or exit
# loop keeps running as we need to keep the program going
while True:
     to_send = input('->')
     if to_send.lower() == 'exit': 
          break
     sent: lynxy.Message = client.send(to_send)
     print('sent:', sent.content)
client.close()