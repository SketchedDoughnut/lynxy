from src import lynxy
import pyautogui

client = lynxy.Lynxy(bind=True)
print('host:', client.get_host())
target = ['192.168.68.113', 56774]
client.connect(target)

@client.event(lynxy.Constants.Event.ON_MESSAGE)
def on_message(data: lynxy.Pool.Message):
    pyautogui.press(data.content)

while True: pass