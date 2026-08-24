# import lynxy
import lynxy

# create our client
client = lynxy.Client()

# add our on_connect event
@client.event(lynxy.Event.ON_CONNECT)
def my_function(connect_state: bool):
     print(input)

# add our on_message event
@client.event(lynxy.Event.ON_MESSAGE)
def my_function(message: lynxy.Message):
     print(message.content)

# add our on_close event
@client.event(lynxy.Event.ON_DISCONNECT)
def my_function(error: Exception| None):
     print(error)

# connect to the other computer using its IP and port
target = ('123.456.78.910', 12345)
lynxy.connect(target)

# send messages, or exit
# loop keeps running as we need to keep the program going
while True:
     to_send = input('->')
     if to_send.lower() == 'exit': 
          break
     sent: lynxy.Message = client.send(to_send)
     print('sent:', sent.content)
client.close()