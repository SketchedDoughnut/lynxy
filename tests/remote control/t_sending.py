from src import lynxy
import keyboard

client = lynxy.Lynxy(bind=True)
target = ['192.168.68.121', 56774]
print('host:', client.get_host())
print('target:', target)
client.connect(target)
print('connected:', client.get_actual_target())

@client.event(lynxy.Constants.Event.ON_CLOSE)
def on_close(error: lynxy.Exceptions.BaseLynxyException):
    print(error)
    
while True:
    pressed = keyboard.read_key()
    print('pressed:', pressed)
    client.send(pressed)