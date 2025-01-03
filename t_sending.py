from src import lynxy
import keyboard

client = lynxy.Lynxy(bind=True)
target = ['192.168.68.121', 56774]
print('host:', client.get_host())
print('target:', target)
client.connect(target)
print('connected:', client.get_actual_target())

while True:
    pressed = keyboard.read_key()
    print('pressed:', pressed)
    client.send(pressed)