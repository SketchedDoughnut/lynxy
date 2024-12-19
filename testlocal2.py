from src import lynxy

# set up instance
inst = lynxy.Lynxy()
# inst.connect('', 0)
# inst.send('test')

# set up a decorator for the on_message event
@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def event(data: lynxy.Pool.Message):
    print(data.content)
    print(data.created_at)
    print(data.recieved_at)

# set up a decorator for the on_close event
@inst.event(lynxy.Constants.Event.ON_CLOSE)
def close(data):
    print(data)

# set up a decorator for the on_connect event
@inst.event(lynxy.Constants.Event.ON_CONNECT)
def connect(data):
    print(data)

inst.set_connection(lynxy.Constants.ConnectionType.EVENT)
inst._comm._trigger(lynxy.Constants.Event.ON_CONNECT, True)
inst._comm._trigger(lynxy.Constants.Event.ON_MESSAGE, lynxy.Pool.Message('message data!'))