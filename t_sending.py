from src import lynxy
import keyboard

client = lynxy.Lynxy(bind=True)
print('host:', client.get_host())
target = ['192.168.68.121', 56774]
client.connect(target)

while True:
    pressed = keyboard.read_key()
    client.send(pressed)