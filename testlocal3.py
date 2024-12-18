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
    print(data.public_key)

# set up a decorator for the on_close event
@inst.event(lynxy.Constants.Event.ON_CLOSE)
def close(data: Exception):
    print(data)


inst.set_connection(lynxy.Constants.ConnectionType.EVENT)
inst._comm._connection_error(lynxy.Exceptions.TerminationSuccessError)