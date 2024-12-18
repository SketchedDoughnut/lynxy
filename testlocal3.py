from src import lynxy
import time
inst = lynxy.Lynxy()
@inst.event(lynxy.Constants.Event.ON_MESSAGE)
def event(data: lynxy.Pool.Message):
    time.sleep(2)
    data.recieved_at = lynxy.Pool.Tools._format_time()
    print(data.content)
    print(data.created_at)
    print(data.recieved_at)
    print(data.public_key)
inst._comm._trigger(lynxy.Constants.Event.ON_MESSAGE, lynxy.Pool.Message('uwu', 'uwu'))