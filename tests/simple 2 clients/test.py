from src import lynxy

host = ('', 56774)
target = ('192.168.86.53', 56775)
cl = lynxy.Lynxy(host=host)


@cl.event(lynxy.Event.ON_MESSAGE)
def msg(msg: lynxy.Message):
    print(msg.content)
    print(msg.created_at)
    print(msg.received_at)


input('connect?')
cl.connect(target)
input('close?')
cl.close()