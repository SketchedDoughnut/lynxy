from src import lynxy

host = ('', 56775)
target = ('192.168.86.53', 56774)
cl = lynxy.Lynxy(host=host)


@cl.event(lynxy.Event.ON_CONNECT)
def cn(s: bool):
    cl.send('hi')


input('connect?')
cl.connect(target)
input('close?')
cl.close()