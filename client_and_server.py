# other imports
import pygame
import random
import time
import threading

# lynxy imports
from src import lynxy as l, lynxy_server as ls

screen_width = 500
screen_height = 500
screen_dimensions = (screen_width, screen_height)

pygame.init()
window = pygame.display.set_mode(screen_dimensions)

def gen_square():
    width = 50
    height = 50
    x = random.randint(0, screen_width - width)
    y = random.randint(0, screen_height - height)
    rect = pygame.Rect(x, y, width, height)
    return rect

# ONLY FOR THE SERVER MACHINE
def start_server() -> tuple:
    ip, port, token = ls.start_server()
    return ip, port, token

def start_connection(ip):
    success = l.start_client(ip)
    print(f'Connection status: {success}')



def send_rect():
    while True:
        time.sleep(1) 
        l.send_msg(rect1, rm)
        # print('sent:', rect)

def gen_new():
    global rect1
    while True:
        time.sleep(5)
        rect1 = ((255, 0, 0), gen_square())

def recieve_handler():
    while True:
        global rect2
        try:
            # print('setting rect2 to -1 of message queue')
            rect2 = l.message_queue[-1]
            # print('rect 2 set to:', rect2)
        except Exception as e:
            # print('set rect error:', e)
            pass



###########

# Code for the SENDING

# initialize rect
rect1 = ((255, 0, 0), gen_square()) # this is the local square
rect2 = ((0, 255, 0), gen_square()) # this is the square from the other client
# start server
ip, port, token = ls.start_server()
# start client
# input_ip = input('-> ')
start_connection(ip)
# start_connection(input_ip)
# go into listener mode
# l.send_msg('listener')  
rm = False
l.start_client_listener()
# start threads to send data
threading.Thread(target=lambda:send_rect()).start()
threading.Thread(target=lambda:gen_new()).start()
# start recieving thread
threading.Thread(target=lambda:recieve_handler()).start()
# start game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill((0, 0, 0))
    pygame.draw.rect(window, rect1[0], rect1[1])
    try:
        # print('second rect drawing to:', rect2)
        pygame.draw.rect(window, rect2[0], rect2[1])
    except Exception as e:
        # print('draw error:', e)
        pass
    pygame.display.update()
pygame.quit()
ls.freeze_server()
l.shutdown_client()