from src import lynxy
import pyautogui

client = lynxy.Lynxy(bind=True)
target = ['192.168.68.113', 56774]
print('host:', client.get_host())
print('target:', target)
client.connect(target)
print('connected:', client.get_actual_target())

@client.event(lynxy.Constants.Event.ON_MESSAGE)
def on_message(data: lynxy.Pool.Message):
    print('recv:', data.content)
    # pyautogui.press(data.content)

@client.event(lynxy.Constants.Event.ON_CLOSE)
def on_close(error: lynxy.Exceptions.BaseLynxyException):
    print(error)

while True: 
    input('- >')
    client.close()