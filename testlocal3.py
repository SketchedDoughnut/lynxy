from src import lynxy

# set up instance
inst = lynxy.Lynxy()

# set up a decorator for the on_message event
@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def event(data: lynxy.Pool.Message):
    print(data.content)
    print(data.created_at)
    print(data.recieved_at)
    print(data.public_key)