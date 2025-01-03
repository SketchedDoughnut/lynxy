from src import lynxy
import pyautogui

client = lynxy.Lynxy(bind=True)
target = ['192.168.68.113', 56774]
print('host:', client.get_host())
print('target:', target)
client.connect(target)

@client.event(lynxy.Constants.Event.ON_MESSAGE)
def on_message(data: lynxy.Pool.Message):
    print('recv:', data.content)
    # pyautogui.press(data.content)

while True: pass