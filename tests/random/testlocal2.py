from src import lynxy

# set up instance
inst = lynxy.Lynxy()
# inst.connect('', 0)
# inst.send('test')

# inst.close
# inst.connect
# inst.event
# inst.get_actual_target
# inst.get_host
# inst.recv
# inst.send

# set up a decorator for the on_message event
@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def on_message(data: lynxy.Pool.Message):
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